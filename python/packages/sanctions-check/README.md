# xyz17711-sanctions-check

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-sanctions-check)](https://pypi.org/project/xyz17711-sanctions-check/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-sanctions-check)](https://pypi.org/project/xyz17711-sanctions-check/)
[![License](https://img.shields.io/pypi/l/xyz17711-sanctions-check)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **🚫 sanctions-check-service**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[sanctions-check]"
```

## Methods

| Method | Description |
| --- | --- |
| `screen_name` | Sanctions check: OFAC list check and sanctions screening of a person or company name against OFAC SDN, EU and UN lists (AML KYC) ($0.01, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`ascreen_name` next to `screen_name`), sharing one underlying client.

## Quickstart

```python
from xyz17711_sanctions_check import Client

client = Client("https://api.17711.xyz/registry/🚫 sanctions-check-service")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-sanctions-check[langchain]"
```

```python
from xyz17711_sanctions_check import Client
from xyz17711_sanctions_check.langchain_tools import SanctionsCheckToolkit

client = Client("https://api.17711.xyz/registry/🚫 sanctions-check-service")
tools = SanctionsCheckToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
