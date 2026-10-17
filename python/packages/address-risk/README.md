# xyz17711-address-risk

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-address-risk)](https://pypi.org/project/xyz17711-address-risk/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-address-risk)](https://pypi.org/project/xyz17711-address-risk/)
[![License](https://img.shields.io/pypi/l/xyz17711-address-risk)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **address-risk-service**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[address-risk]"
```

## Methods

| Method | Description |
| --- | --- |
| `check_address` | Wallet address risk check: sanctioned address and phishing check for a crypto wallet or contract before you send funds, with theft, scam, mixer and blacklist flags ($0.005, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`acheck_address` next to `check_address`), sharing one underlying client.

## Quickstart

```python
from xyz17711_address_risk import Client

client = Client("https://api.17711.xyz/registry/address-risk-service")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-address-risk[langchain]"
```

```python
from xyz17711_address_risk import Client
from xyz17711_address_risk.langchain_tools import AddressRiskToolkit

client = Client("https://api.17711.xyz/registry/address-risk-service")
tools = AddressRiskToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
