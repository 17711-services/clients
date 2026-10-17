# xyz17711-ping

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-ping)](https://pypi.org/project/xyz17711-ping/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-ping)](https://pypi.org/project/xyz17711-ping/)
[![License](https://img.shields.io/pypi/l/xyz17711-ping)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **ping-service**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[ping]"
```

## Methods

| Method | Description |
| --- | --- |
| `ping` | x402 ping: the cheapest end-to-end payment test for an x402 client or agent wallet, returns an echo and the server pid ($0.002, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`aping` next to `ping`), sharing one underlying client.

## Quickstart

```python
from xyz17711_ping import Client

client = Client("https://api.17711.xyz/registry/ping-service")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-ping[langchain]"
```

```python
from xyz17711_ping import Client
from xyz17711_ping.langchain_tools import PingToolkit

client = Client("https://api.17711.xyz/registry/ping-service")
tools = PingToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
