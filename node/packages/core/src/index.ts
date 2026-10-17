/**
 * Core HTTP client for the 17711.xyz microservice fleet -- shared transport, auth, x402 payment,
 * and error handling every per-service generated client package builds on. Not meant to be used
 * directly beyond that.
 *
 * Every generated method is async (JS has no separate sync path, unlike the Python client's
 * sync+async pair) -- one method per operation is enough here.
 *
 * x402 payment logic here implements the real x402 v2 protocol end to end: the same wire format
 * (three headers, base64-encoded JSON) and the same EIP-3009 `transferWithAuthorization` signing
 * over EIP-712 typed data as `xyz17711_core` (Python) and this platform's own Rust buyer side --
 * verified byte-for-byte compatible via a fixed cross-language test vector, not just "looks
 * right" (see `test/x402.test.mjs`). Payment decision/signing is pure, synchronous logic (no
 * `await` between reading and updating the spend tracker) so it never races itself even though
 * JS has no real threads -- see `reserveSpend` below for why that matters.
 */

import { privateKeyToAccount, type PrivateKeyAccount } from "viem/accounts";
import { getAddress } from "viem";
import { randomBytes } from "node:crypto";

const HEADER_PAYMENT_REQUIRED = "PAYMENT-REQUIRED";
const HEADER_PAYMENT_SIGNATURE = "PAYMENT-SIGNATURE";
const USDC_DECIMALS = 6;

/**
 * Mirrors this platform's own standardized error envelope
 * (`{"error": {code, index, status, message}}`) -- every non-2xx response from any 17711.xyz
 * service throws this, never a bare fetch error.
 */
export class PlatformError extends Error {
  code: string;
  index: number;
  status: number;

  constructor(code: string, index: number, status: number, message: string) {
    super(`${code}: ${message}`);
    this.name = "PlatformError";
    this.code = code;
    this.index = index;
    this.status = status;
  }

  static async fromResponse(response: Response): Promise<PlatformError> {
    try {
      const body = (await response.json()) as { error?: Record<string, unknown> };
      const error = body.error ?? {};
      return new PlatformError(
        (error.code as string) ?? "unknown",
        (error.index as number) ?? -1,
        (error.status as number) ?? response.status,
        (error.message as string) ?? response.statusText,
      );
    } catch {
      return new PlatformError("unknown", -1, response.status, response.statusText);
    }
  }
}

/**
 * Thrown when a gated tool's free quota is exhausted and either no wallet is configured on this
 * {@link Client}, or the seller's own accepted network doesn't match `x402ExpectedNetwork`.
 * Carries the decoded `PAYMENT-REQUIRED` challenge so a caller can decide what to do -- this is
 * NOT a generic failure, it's an actionable "pay this much, on this network, to this address"
 * signal.
 */
export class PaymentRequiredError extends PlatformError {
  priceUsdc: number;
  network: string;
  payTo: string;

  constructor(message: string, priceUsdc: number, network: string, payTo: string) {
    super("request.payment_required", -1, 402, message);
    this.name = "PaymentRequiredError";
    this.priceUsdc = priceUsdc;
    this.network = network;
    this.payTo = payTo;
  }
}

/** Thrown by {@link Client}'s constructor when `x402PrivateKey` is set but the rest of the wallet
 * config is missing -- a half-configured wallet with real funds behind it is worse to silently
 * half-work than to refuse to construct. */
export class WalletConfigError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "WalletConfigError";
  }
}

function decodeHeader(value: string): Record<string, unknown> | null {
  try {
    return JSON.parse(Buffer.from(value.trim(), "base64").toString("utf8"));
  } catch {
    return null;
  }
}

function encodeHeader(value: unknown): string {
  return Buffer.from(JSON.stringify(value), "utf8").toString("base64");
}

function parseEip155ChainId(network: string): number {
  if (!network.startsWith("eip155:")) {
    throw new PlatformError(
      "payment.invalid",
      -1,
      500,
      `malformed network id (expected CAIP-2 "eip155:<chain_id>"): ${network}`,
    );
  }
  return Number(network.slice("eip155:".length));
}

// Cumulative x402 spend is tracked per WALLET ADDRESS, module-level, shared by every `Client`
// instance in this process -- never a per-instance counter. Mirrors both the Rust reference
// implementation's global `Mutex<f64>` and `xyz17711_core`'s own per-address/lock design: the
// idiomatic way to use this SDK is one `Client` per service, so a per-instance counter would let
// the SAME wallet silently spend its configured cap once per client instead of once, total.
// JS has no real threads, so no explicit lock is needed -- but the check-then-reserve below MUST
// stay synchronous (no `await` between the read and the write) or a future change reintroducing
// concurrency here could reopen the exact race a lock would otherwise prevent.
const cumulativeSpentByAddress = new Map<string, number>();

export interface ClientOptions {
  /** Pass to sign and pay past the free quota automatically -- requires the three other
   * `x402*` options, all together or none. Never read from an env var by this class itself; the
   * caller sources it from wherever it lives (an env var, a secrets manager) and never logs it. */
  x402PrivateKey?: string;
  /** CAIP-2 network id this wallet expects to pay on (e.g. `"eip155:8453"` for Base mainnet) --
   * a seller quoting a different network raises {@link PaymentRequiredError} instead of silently
   * paying on the wrong chain. */
  x402ExpectedNetwork?: string;
  /** Refuses any single payment above this many USDC. */
  x402MaxPaymentUsdc?: number;
  /** Refuses once this WALLET's (not just this `Client` instance's) lifetime spend in this
   * process would exceed this many USDC -- see `cumulativeSpentByAddress` above. */
  x402MaxTotalSpendUsdc?: number;
}

/**
 * Base HTTP client for one 17711.xyz service instance. Per-service generated client classes
 * (e.g. `@xyz17711/proxy-pool`'s `Client`) extend this and add one typed method per tool.
 */
export class Client {
  protected baseUrl: string;
  private headers: Record<string, string>;
  private account: PrivateKeyAccount | null = null;
  private x402ExpectedNetwork?: string;
  private x402MaxPaymentUsdc?: number;
  private x402MaxTotalSpendUsdc?: number;

  constructor(baseUrl: string, options: ClientOptions = {}) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.headers = { "content-type": "application/json" };
    this.x402ExpectedNetwork = options.x402ExpectedNetwork;
    this.x402MaxPaymentUsdc = options.x402MaxPaymentUsdc;
    this.x402MaxTotalSpendUsdc = options.x402MaxTotalSpendUsdc;

    if (options.x402PrivateKey) {
      const missing = (
        [
          ["x402ExpectedNetwork", options.x402ExpectedNetwork],
          ["x402MaxPaymentUsdc", options.x402MaxPaymentUsdc],
          ["x402MaxTotalSpendUsdc", options.x402MaxTotalSpendUsdc],
        ] as const
      )
        .filter(([, v]) => v === undefined)
        .map(([k]) => k);
      if (missing.length > 0) {
        throw new WalletConfigError(
          `x402PrivateKey was set but ${missing.join(", ")} -- a wallet with real funds needs ` +
            "explicit per-call and cumulative spend caps and an expected network, all set " +
            "together, or none at all.",
        );
      }
      const key = options.x402PrivateKey.startsWith("0x")
        ? (options.x402PrivateKey as `0x${string}`)
        : (`0x${options.x402PrivateKey}` as `0x${string}`);
      this.account = privateKeyToAccount(key);
    }
  }

  protected async post<T>(path: string, body: unknown): Promise<T> {
    return this.requestWithPayment((headers) =>
      fetch(`${this.baseUrl}${path}`, {
        method: "POST",
        headers: { ...this.headers, ...headers },
        body: JSON.stringify(body),
      }),
    );
  }

  protected async get<T>(path: string, params: Record<string, unknown>): Promise<T> {
    const query = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== null) {
        query.set(key, String(value));
      }
    }
    const qs = query.toString();
    return this.requestWithPayment((headers) =>
      fetch(`${this.baseUrl}${path}${qs ? `?${qs}` : ""}`, {
        headers: { ...this.headers, ...headers },
      }),
    );
  }

  private async requestWithPayment<T>(
    send: (headers: Record<string, string>) => Promise<Response>,
  ): Promise<T> {
    const first = await send({});
    if (first.status !== 402) {
      if (!first.ok) {
        throw await PlatformError.fromResponse(first);
      }
      return (await first.json()) as T;
    }

    const signedHeader = await this.handle402(first);
    const second = await send({ [HEADER_PAYMENT_SIGNATURE]: signedHeader });
    if (!second.ok) {
      throw await PlatformError.fromResponse(second);
    }
    return (await second.json()) as T;
  }

  private async handle402(response: Response): Promise<string> {
    const headerValue = response.headers.get(HEADER_PAYMENT_REQUIRED);
    if (!headerValue) {
      throw new PlatformError(
        "payment.invalid",
        -1,
        402,
        "seller returned 402 with no PAYMENT-REQUIRED header",
      );
    }
    const paymentRequired = decodeHeader(headerValue);
    if (paymentRequired === null) {
      throw new PlatformError(
        "payment.invalid",
        -1,
        402,
        "seller's PAYMENT-REQUIRED header did not decode to valid JSON",
      );
    }

    const accepts = (paymentRequired.accepts as Array<Record<string, unknown>>) ?? [];
    const requirements = accepts.find(
      (a) => a.scheme === "exact" && a.network === this.x402ExpectedNetwork,
    );
    const amountUsdc = requirements
      ? Number(requirements.amount as string) / 10 ** USDC_DECIMALS
      : undefined;

    if (!this.account || !requirements) {
      throw new PaymentRequiredError(
        (paymentRequired.error as string) ||
          "this tool's free quota is used up -- sign and send a payment to continue",
        amountUsdc ?? 0,
        this.x402ExpectedNetwork ?? "",
        (requirements?.payTo as string) ?? "",
      );
    }

    if (amountUsdc! > this.x402MaxPaymentUsdc!) {
      throw new PlatformError(
        "payment.rejected",
        -1,
        402,
        `requested amount (${amountUsdc} USDC) exceeds this wallet's configured per-call cap ` +
          "(x402MaxPaymentUsdc)",
      );
    }

    const address = this.account.address;
    // Synchronous check-then-reserve, no `await` in between -- see `cumulativeSpentByAddress`'s
    // own doc comment above for why that's what makes this safe without an explicit lock.
    const spentSoFar = cumulativeSpentByAddress.get(address) ?? 0;
    if (spentSoFar + amountUsdc! > this.x402MaxTotalSpendUsdc!) {
      throw new PlatformError(
        "payment.rejected",
        -1,
        402,
        "paying this would exceed this wallet's configured cumulative cap " +
          "(x402MaxTotalSpendUsdc)",
      );
    }
    cumulativeSpentByAddress.set(address, spentSoFar + amountUsdc!);

    try {
      return await this.signPayment(paymentRequired, requirements);
    } catch (e) {
      cumulativeSpentByAddress.set(address, spentSoFar);
      throw e;
    }
  }

  private async signPayment(
    paymentRequired: Record<string, unknown>,
    requirements: Record<string, unknown>,
  ): Promise<string> {
    const account = this.account!;
    const chainId = parseEip155ChainId(requirements.network as string);
    const now = Math.floor(Date.now() / 1000);
    const validAfter = Math.max(0, now - 60);
    const validBefore = now + Number(requirements.maxTimeoutSeconds);
    const nonceHex = `0x${randomBytes(32).toString("hex")}` as `0x${string}`;
    const extra = requirements.extra as { name: string; version: string };
    const amount = BigInt(requirements.amount as string);

    // viem enforces EIP-55 checksum casing on every address in typed data (throws
    // `InvalidAddressError` otherwise) -- Python's `eth_account` does not, so a seller returning
    // an all-lowercase address (common) works fine there but would throw here without this.
    // Checksumming never changes the signed digest (ABI-encodes to the same 20 raw bytes either
    // way, casing is a display-only convention) -- purely satisfies viem's stricter input
    // validation, confirmed by the cross-language test vector in `test/x402.test.mjs`.
    const signature = await account.signTypedData({
      domain: {
        name: extra.name,
        version: extra.version,
        chainId,
        verifyingContract: getAddress(requirements.asset as string),
      },
      types: {
        TransferWithAuthorization: [
          { name: "from", type: "address" },
          { name: "to", type: "address" },
          { name: "value", type: "uint256" },
          { name: "validAfter", type: "uint256" },
          { name: "validBefore", type: "uint256" },
          { name: "nonce", type: "bytes32" },
        ],
      },
      primaryType: "TransferWithAuthorization",
      message: {
        from: account.address,
        to: getAddress(requirements.payTo as string),
        value: amount,
        validAfter: BigInt(validAfter),
        validBefore: BigInt(validBefore),
        nonce: nonceHex,
      },
    });

    const authorization = {
      from: account.address,
      to: requirements.payTo,
      value: amount.toString(),
      validAfter: String(validAfter),
      validBefore: String(validBefore),
      nonce: nonceHex,
    };
    const payload: Record<string, unknown> = {
      x402Version: paymentRequired.x402Version,
      resource: paymentRequired.resource,
      accepted: requirements,
      payload: { signature, authorization },
    };
    // x402 v2: echo the challenge's `extensions` (notably `bazaar`) back unchanged so the
    // facilitator can catalog the resource once this payment settles. Omitted when absent.
    if (paymentRequired.extensions) {
      payload.extensions = paymentRequired.extensions;
    }
    return encodeHeader(payload);
  }
}

// Exported for the cross-language wire-compatibility test vector (test/x402.test.mjs) -- never
// meant to be used outside this package's own test suite.
export const _internal = { decodeHeader, encodeHeader, cumulativeSpentByAddress };
