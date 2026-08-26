# xyz17711 Python clients

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711)](https://pypi.org/project/xyz17711/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711)](https://pypi.org/project/xyz17711/)
[![License](https://img.shields.io/pypi/l/xyz17711)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python clients for the [17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call
APIs settled in USDC via the [x402](https://x402.org) protocol, listed on
[x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). One package per service, generated directly from that service's own
live OpenAPI document, plus optional LangChain tool wrappers so an agent can call these services
directly.

- **Typed**: every request/response is a real Pydantic model, not a raw dict.
- **Sync and async**: every method has a plain form (`client.ping(...)`) and an async sibling
  (`await client.aping(...)`), sharing one underlying client -- pick whichever fits your code.
- **Pay-as-you-go**: a handful of free calls per service per day, then a small USDC payment per
  call. This client can pay automatically (see below) or just tell you the price and let you
  decide.
- **No accounts, no API keys** -- x402 payment (or staying within the free quota) is the only
  auth this fleet needs.

## Install

```bash
pip install "xyz17711[ping]"          # core client + the ping service's own package
pip install "xyz17711[proxy-pool]"    # core client + the proxy-pool service's own package
```

Every available service:

- `emoji-match` -- `pip install "xyz17711[emoji-match]"`
- `ip-blocklist` -- `pip install "xyz17711[ip-blocklist]"`
- `ping` -- `pip install "xyz17711[ping]"`
- `proxy-pool` -- `pip install "xyz17711[proxy-pool]"`
- `web-scraper` -- `pip install "xyz17711[web-scraper]"`
- `websearch` -- `pip install "xyz17711[websearch]"`

Each service is its own optional extra of the `xyz17711` core package -- installing one never
pulls in the others. Add the `payments` extra to pay automatically past the free quota:

```bash
pip install "xyz17711[payments]"
```

Add the `langchain` extra on a SPECIFIC service package (not on `xyz17711` itself) to get that
service's LangChain tools:

```bash
pip install "xyz17711-ping[langchain]"
```

## Quickstart

```python
from xyz17711_ping import Client, PingRequest

client = Client("https://api.17711.xyz/registry/ping-service")
result = client.ping(PingRequest(echo="hello"))
print(result.echo, result.pid)
```

Async, on the exact same client:

```python
import asyncio
from xyz17711_ping import Client, PingRequest

async def main():
    async with Client("https://api.17711.xyz/registry/ping-service") as client:
        result = await client.aping(PingRequest(echo="hello"))
        print(result.echo, result.pid)

asyncio.run(main())
```

## Paying past the free quota

Every gated tool allows a small number of free calls per day; beyond that it returns a 402
challenge. Without a wallet configured, this client raises `PaymentRequiredError` with the price,
network, and payee address attached -- decide what to do with that information yourself:

```python
from xyz17711_core.client import PaymentRequiredError

try:
    client.ping(PingRequest(echo="hello"))
except PaymentRequiredError as e:
    print(f"needs {e.price_usdc} USDC on {e.network}, payable to {e.pay_to}")
```

To pay automatically (requires `pip install "xyz17711[payments]"`), configure a wallet on the
client -- the private key should come from your own environment/secrets manager, never a literal
string in source code:

```python
import os
from xyz17711_ping import Client

client = Client(
    "https://api.17711.xyz/registry/ping-service",
    x402_private_key=os.environ["X402_PRIVATE_KEY"],
    x402_expected_network="eip155:8453",       # Base mainnet; use eip155:84532 for Base Sepolia testnet
    x402_max_payment_usdc=0.01,                # refuse any single call above this
    x402_max_total_spend_usdc=1.0,             # refuse once this WALLET's lifetime spend would exceed it
)
```

**Never commit a private key.** Both spend caps are required together with the key -- a wallet
with real funds and no explicit caps refuses to construct at all (`WalletConfigError`), on
purpose. The cumulative cap is tracked per wallet address, shared by every `Client` you construct
with that same key in this process -- not reset just because you built a second `Client`.

## LangChain

Each service package exposes a `BaseToolkit` (from `langchain_core.tools`) grouping one
`StructuredTool` per operation -- each tool supports both `.invoke()` and `.ainvoke()`.

```python
from xyz17711_ping import Client
from xyz17711_ping.langchain_tools import PingToolkit

client = Client("https://api.17711.xyz/registry/ping-service", x402_private_key=..., ...)
tools = PingToolkit(client=client).get_tools()

# use directly
tools[0].invoke({"echo": "hello"})

# or hand the list to an agent
from langchain.agents import create_agent
agent = create_agent(model="...", tools=tools)
```

A `PaymentRequiredError` raised by a tool propagates like any other exception -- pair it with
LangChain's own [human-in-the-loop
middleware](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) if you want a human
to approve a real spend before it happens.

## Logging

Every module logs through the standard library (`logging.getLogger(__name__)`) -- nothing is
configured for you. Enable it like any other library:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Errors

Every non-2xx response raises `xyz17711_core.client.PlatformError` (or its `PaymentRequiredError`
subclass for a 402), carrying the same `code`/`index`/`status`/`message` the service itself
returned -- never a bare HTTP exception.

## About the generated packages

Every package under `packages/<service>/` -- including its `tests/` -- is generated directly from
that service's own live OpenAPI document, never hand-written, by tooling that lives in this
project's internal monorepo (not part of this public repo). If a service's API changes, the
maintainers regenerate and republish the affected package; this repo's own `packages/<service>/`
directories are the generated OUTPUT, meant to be read and used, not hand-edited or regenerated by
external contributors. Found a bug or an API change that hasn't been picked up yet? Open an issue.

## Running the tests

```bash
pip install -e packages/core[test] -e packages/<service>[langchain]
pytest packages/<service>/tests/
```

Run one package at a time -- two packages both have a `tests/test_client.py`, and running them
together in a single `pytest` invocation confuses its import machinery.

## License

MIT -- see [`LICENSE`](../LICENSE), shared by every language's client library in the
`clients` repo this package lives in.
