# xyz17711-token-verdict

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-token-verdict)](https://pypi.org/project/xyz17711-token-verdict/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-token-verdict)](https://pypi.org/project/xyz17711-token-verdict/)
[![License](https://img.shields.io/pypi/l/xyz17711-token-verdict)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **token-verdict-service**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[token-verdict]"
```

## Methods

| Method | Description |
| --- | --- |
| `get_verdict` | Token verdict and security check: is this token safe? Honeypot, rug pull and scam detection with taxes, liquidity and admin powers ($0.01, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`aget_verdict` next to `get_verdict`), sharing one underlying client.

## Quickstart

```python
from xyz17711_token_verdict import Client

client = Client("https://api.17711.xyz/registry/token-verdict-service")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-token-verdict[langchain]"
```

```python
from xyz17711_token_verdict import Client
from xyz17711_token_verdict.langchain_tools import TokenVerdictToolkit

client = Client("https://api.17711.xyz/registry/token-verdict-service")
tools = TokenVerdictToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
