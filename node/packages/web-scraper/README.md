# @xyz17711/web-scraper

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-node.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-node.yml)
[![npm](https://img.shields.io/npm/v/@xyz17711/web-scraper)](https://www.npmjs.com/package/@xyz17711/web-scraper)
[![License](https://img.shields.io/npm/l/@xyz17711/web-scraper)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed TypeScript client for **web-scraper**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff).

## Install

```bash
npm install @xyz17711/web-scraper
```

## Methods

| Method | Description |
| --- | --- |
| `extractMarkdown` | URL to Markdown: read any web page and get its main article content as clean Markdown for agents ($0.003, x402) |
| `getTaskStatus` | Polls for the result of a task enqueued by a *_async tool |
| `scrapeUrl` | Scrape URL: fetch any web page through a proxy and get its status, content type and raw HTML ($0.002, x402) |
| `scrapeUrlAsync` | [Deprecated - use web_scraper_scrape_url] Enqueues a web_scraper_scrape_url job and returns a task id immediately ($0.002, x402) |

## Quickstart

```typescript
import { Client } from "@xyz17711/web-scraper";

const client = new Client(); // talks to https://api.17711.xyz/registry/web-scraper by default
// see the Methods table above for every available call and its request/response type
```

Pass another base URL (self-hosted instance, test server) as the first argument:
`new Client("https://my-host.example/registry/web-scraper")`.

## Paying past the free quota

Every gated tool allows a small number of free calls per day; beyond that it returns a 402
challenge. Without a wallet configured, this client throws `PaymentRequiredError` with the price,
network, and payee address attached:

```typescript
import { Client, PaymentRequiredError } from "@xyz17711/web-scraper";

const client = new Client();
try {
  await client.extractMarkdown(/* ... */);
} catch (e) {
  if (e instanceof PaymentRequiredError) {
    console.log(`needs ${e.priceUsdc} USDC on ${e.network}, payable to ${e.payTo}`);
  }
}
```

To pay automatically, configure a wallet on the client -- the private key should come from your
own environment/secrets manager, never a literal string in source code:

```typescript
import { Client } from "@xyz17711/web-scraper";

const client = new Client({
  x402PrivateKey: process.env.X402_PRIVATE_KEY,
  x402ExpectedNetwork: "eip155:8453", // Base mainnet; use eip155:84532 for Base Sepolia testnet
  x402MaxPaymentUsdc: 0.01,           // refuse any single call above this
  x402MaxTotalSpendUsdc: 1.0,         // refuse once this WALLET's lifetime spend would exceed it
});
```

**Never commit a private key.** Both spend caps are required together with the key -- a wallet
with real funds and no explicit caps refuses to construct at all (`WalletConfigError`), on
purpose. The cumulative cap is tracked per wallet address, shared by every `Client` you construct
with that same key in this process.

## LangChain.js

```typescript
import { Client } from "@xyz17711/web-scraper";
import { WebScraperToolkit } from "@xyz17711/web-scraper/langchain";

const client = new Client({ /* ...wallet options... */ });
const tools = new WebScraperToolkit(client).getTools();
```

Requires the optional `@langchain/core`+`zod` peer dependencies (`npm install @langchain/core
zod`) -- importing the base package above never requires them; only `@xyz17711/web-scraper/langchain`
does.

## License

MIT -- see [`LICENSE`](../../LICENSE), shared by every language's client library in the
`clients` repo this package lives in.
