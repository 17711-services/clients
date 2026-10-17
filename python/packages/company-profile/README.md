# xyz17711-company-profile

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-company-profile)](https://pypi.org/project/xyz17711-company-profile/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-company-profile)](https://pypi.org/project/xyz17711-company-profile/)
[![License](https://img.shields.io/pypi/l/xyz17711-company-profile)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **company-profile-service**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[company-profile]"
```

## Methods

| Method | Description |
| --- | --- |
| `get_profile` | Company profile and enrichment from a domain or a name: offering, public contacts, social links and WHOIS domain data as valid JSON ($0.009, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`aget_profile` next to `get_profile`), sharing one underlying client.

## Quickstart

```python
from xyz17711_company_profile import Client

client = Client("https://api.17711.xyz/registry/company-profile-service")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-company-profile[langchain]"
```

```python
from xyz17711_company_profile import Client
from xyz17711_company_profile.langchain_tools import CompanyProfileToolkit

client = Client("https://api.17711.xyz/registry/company-profile-service")
tools = CompanyProfileToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
