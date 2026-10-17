/**
 * Real functional tests for @xyz17711/core's x402 payment port -- the EIP-712 signing/spend-cap
 * logic in particular, since that's genuinely new code, not a thin wrapper. Uses a fake
 * `globalThis.fetch` throughout -- no real network call, no real blockchain interaction -- but
 * the signing path itself is real (a freshly-derived test account), so a malformed signature
 * would be caught here.
 */

import { test } from "node:test";
import assert from "node:assert/strict";
import { privateKeyToAccount } from "viem/accounts";
import { Client, PaymentRequiredError, PlatformError, WalletConfigError, _internal } from "../dist/index.js";

const TEST_PRIVATE_KEY = `0x${"11".repeat(32)}`;
const TEST_ADDRESS = privateKeyToAccount(TEST_PRIVATE_KEY).address;

const PAYMENT_REQUIRED_BODY = {
  x402Version: 2,
  error: "PAYMENT-SIGNATURE header is required",
  resource: { url: "https://example.test/tool", description: "", mimeType: "application/json" },
  accepts: [
    {
      scheme: "exact",
      network: "eip155:84532",
      amount: "10000",
      asset: "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
      payTo: "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
      maxTimeoutSeconds: 60,
      extra: { name: "USDC", version: "2" },
    },
  ],
};

function paymentRequiredResponse() {
  return new Response(null, {
    status: 402,
    headers: { "PAYMENT-REQUIRED": _internal.encodeHeader(PAYMENT_REQUIRED_BODY) },
  });
}

function mockFetch(handler) {
  return async (url, init = {}) => handler(new URL(url), init);
}

function withWallet(overrides = {}) {
  return {
    x402PrivateKey: TEST_PRIVATE_KEY,
    x402ExpectedNetwork: "eip155:84532",
    x402MaxPaymentUsdc: 1.0,
    x402MaxTotalSpendUsdc: 100.0,
    ...overrides,
  };
}

class TestClient extends Client {
  callPost(path, body) {
    return this.post(path, body);
  }
}

test.beforeEach(() => {
  _internal.cumulativeSpentByAddress.clear();
});

// --- header codec ---------------------------------------------------------------------------

test("header codec round-trips a real payload", () => {
  const encoded = _internal.encodeHeader(PAYMENT_REQUIRED_BODY);
  assert.deepEqual(_internal.decodeHeader(encoded), PAYMENT_REQUIRED_BODY);
});

test("header codec returns null for garbage", () => {
  assert.equal(_internal.decodeHeader("not valid base64 or json!!!"), null);
});

// --- cross-language wire/crypto compatibility ------------------------------------------------
// A FIXED input vector (private key, addresses, amounts, nonce) signed independently by both
// `xyz17711_core` (Python, via eth_account) and this client (via viem) -- both must produce the
// EXACT same signature bytes, or the two SDKs would be silently incompatible with the real
// facilitator despite each "looking right" in isolation.
test("EIP-712 signature is byte-for-byte identical to the Python/eth_account reference", async () => {
  const account = privateKeyToAccount(`0x${"11".repeat(32)}`);
  assert.equal(account.address, "0x19E7E376E7C213B7E7e7e46cc70A5dD086DAff2A");

  const { getAddress } = await import("viem");
  const signature = await account.signTypedData({
    domain: {
      name: "USD Coin",
      version: "2",
      chainId: 8453,
      verifyingContract: getAddress("0x8335c86C82E7DB0Ea6fc7C9666D1D1c1a0b1B1D0"),
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
      to: getAddress("0x209693Bc6afc0C5328bA36FaF03C514EF312287C"),
      value: 10000n,
      validAfter: 1700000000n,
      validBefore: 1700000060n,
      nonce: `0x${"22".repeat(32)}`,
    },
  });

  assert.equal(
    signature,
    "0x98b408d6f5d67e7345fde7324ff129362eeb61352b626ad27b544ec1ff9e431a6c280fb4552d78a59043e39571b2dc42c805f85984b878bac07dfd8f96a6c4601b",
  );
});

// --- no wallet configured ---------------------------------------------------------------------

test("post without a wallet raises PaymentRequiredError on a 402", async () => {
  globalThis.fetch = mockFetch(() => paymentRequiredResponse());
  const client = new TestClient("https://example.test");
  await assert.rejects(() => client.callPost("/v1/tool", {}), PaymentRequiredError);
});

// --- successful payment + retry -----------------------------------------------------------

function paidHandlerFactory() {
  const calls = { n: 0 };
  const handler = async (_url, init) => {
    calls.n += 1;
    const sig = init.headers?.["PAYMENT-SIGNATURE"];
    if (sig) {
      const payload = _internal.decodeHeader(sig);
      assert.equal(payload.x402Version, 2);
      assert.equal(payload.accepted.network, "eip155:84532");
      assert.equal(payload.payload.authorization.from.toLowerCase(), TEST_ADDRESS.toLowerCase());
      assert.equal(payload.payload.authorization.to, "0x209693Bc6afc0C5328bA36FaF03C514EF312287C");
      assert.equal(payload.payload.authorization.value, "10000");
      assert.ok(payload.payload.signature.startsWith("0x"));
      assert.equal(payload.payload.signature.length, 2 + 130);
      return new Response(JSON.stringify({ ok: true }), { status: 200 });
    }
    return paymentRequiredResponse();
  };
  return { handler, calls };
}

test("post pays and retries on a 402", async () => {
  const { handler, calls } = paidHandlerFactory();
  globalThis.fetch = mockFetch(handler);
  const client = new TestClient("https://example.test", withWallet());
  const result = await client.callPost("/v1/tool", {});
  assert.deepEqual(result, { ok: true });
  assert.equal(calls.n, 2);
  assert.ok(Math.abs(_internal.cumulativeSpentByAddress.get(TEST_ADDRESS) - 0.01) < 1e-9);
});

// --- extensions echo ------------------------------------------------------------------------

test("the challenge's extensions (bazaar) are echoed unchanged in the signed payload", async () => {
  const extensions = { bazaar: { info: { input: { type: "http", method: "POST" } } } };
  let seen;
  globalThis.fetch = mockFetch(async (_url, init) => {
    const sig = new Headers(init.headers).get("PAYMENT-SIGNATURE");
    if (sig) {
      seen = _internal.decodeHeader(sig);
      return new Response(JSON.stringify({ ok: true }), { status: 200 });
    }
    return new Response(null, {
      status: 402,
      headers: {
        "PAYMENT-REQUIRED": _internal.encodeHeader({ ...PAYMENT_REQUIRED_BODY, extensions }),
      },
    });
  });
  const client = new TestClient("https://example.test", withWallet());
  await client.callPost("/v1/tool", {});
  assert.deepEqual(seen.extensions, extensions);
});

test("no extensions key in the payload when the challenge carries none", async () => {
  let seen;
  globalThis.fetch = mockFetch(async (_url, init) => {
    const sig = new Headers(init.headers).get("PAYMENT-SIGNATURE");
    if (sig) {
      seen = _internal.decodeHeader(sig);
      return new Response(JSON.stringify({ ok: true }), { status: 200 });
    }
    return paymentRequiredResponse();
  });
  const client = new TestClient("https://example.test", withWallet());
  await client.callPost("/v1/tool", {});
  assert.equal("extensions" in seen, false);
});

// --- caps and validation --------------------------------------------------------------------

test("per-call cap rejects before a second request is ever sent", async () => {
  const calls = { n: 0 };
  globalThis.fetch = mockFetch(async () => {
    calls.n += 1;
    return paymentRequiredResponse();
  });
  const client = new TestClient("https://example.test", withWallet({ x402MaxPaymentUsdc: 0.001 }));
  await assert.rejects(
    () => client.callPost("/v1/tool", {}),
    (err) => err instanceof PlatformError && err.code === "payment.rejected",
  );
  assert.equal(calls.n, 1);
});

test("cumulative cap rejects the second call", async () => {
  const { handler } = paidHandlerFactory();
  globalThis.fetch = mockFetch(handler);
  const client = new TestClient("https://example.test", withWallet({ x402MaxTotalSpendUsdc: 0.015 }));
  await client.callPost("/v1/tool", {}); // first call: 0.01 USDC, within the 0.015 cap
  await assert.rejects(
    () => client.callPost("/v1/tool", {}), // second call would bring total to 0.02 > 0.015
    (err) => err instanceof PlatformError && err.code === "payment.rejected",
  );
});

test("cumulative cap is shared across Client instances for the same wallet", async () => {
  const { handler } = paidHandlerFactory();
  globalThis.fetch = mockFetch(handler);
  const clientA = new TestClient("https://example.test", withWallet({ x402MaxTotalSpendUsdc: 0.015 }));
  const clientB = new TestClient("https://example.test", withWallet({ x402MaxTotalSpendUsdc: 0.015 }));
  await clientA.callPost("/v1/tool", {}); // 0.01 USDC via clientA, within the shared 0.015 cap
  await assert.rejects(
    () => clientB.callPost("/v1/tool", {}), // same wallet, a DIFFERENT instance -- still capped
    (err) => err instanceof PlatformError && err.code === "payment.rejected",
  );
});

test("different wallets have independent cumulative caps", async () => {
  const handler = async (_url, init) => {
    const sig = init.headers?.["PAYMENT-SIGNATURE"];
    return sig ? new Response(JSON.stringify({ ok: true }), { status: 200 }) : paymentRequiredResponse();
  };
  globalThis.fetch = mockFetch(handler);
  const keyA = `0x${"33".repeat(32)}`;
  const keyB = `0x${"44".repeat(32)}`;
  const clientA = new TestClient(
    "https://example.test",
    withWallet({ x402PrivateKey: keyA, x402MaxTotalSpendUsdc: 0.015 }),
  );
  const clientB = new TestClient(
    "https://example.test",
    withWallet({ x402PrivateKey: keyB, x402MaxTotalSpendUsdc: 0.015 }),
  );
  await clientA.callPost("/v1/tool", {});
  await clientB.callPost("/v1/tool", {}); // a different wallet -- must not be blocked by clientA's spend
});

test("network mismatch raises PaymentRequiredError, not a silent wrong-chain payment", async () => {
  globalThis.fetch = mockFetch(async () => paymentRequiredResponse());
  const client = new TestClient(
    "https://example.test",
    withWallet({ x402ExpectedNetwork: "eip155:1" }),
  );
  await assert.rejects(() => client.callPost("/v1/tool", {}), PaymentRequiredError);
});

test("incoherent wallet config throws at construction", () => {
  for (const missing of ["x402ExpectedNetwork", "x402MaxPaymentUsdc", "x402MaxTotalSpendUsdc"]) {
    const options = withWallet({ [missing]: undefined });
    assert.throws(() => new TestClient("https://example.test", options), WalletConfigError);
  }
});

test("no wallet at all is a valid configuration", () => {
  assert.doesNotThrow(() => new TestClient("https://example.test"));
});

// --- regression against non-payment behavior ------------------------------------------------

test("a plain 2xx success is unaffected", async () => {
  globalThis.fetch = mockFetch(async () => new Response(JSON.stringify({ echoed: "hi" }), { status: 200 }));
  const client = new TestClient("https://example.test");
  assert.deepEqual(await client.callPost("/v1/echo", { x: 1 }), { echoed: "hi" });
});

test("a plain non-402 error still raises PlatformError, not PaymentRequiredError", async () => {
  globalThis.fetch = mockFetch(
    async () =>
      new Response(
        JSON.stringify({
          error: { code: "internal.unhandled", index: 9999, status: 500, message: "boom" },
        }),
        { status: 500 },
      ),
  );
  const client = new TestClient("https://example.test");
  await assert.rejects(
    () => client.callPost("/v1/echo", {}),
    (err) => err instanceof PlatformError && !(err instanceof PaymentRequiredError) && err.code === "internal.unhandled",
  );
});
