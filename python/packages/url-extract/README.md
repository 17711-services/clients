# xyz17711-url-extract

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-url-extract)](https://pypi.org/project/xyz17711-url-extract/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-url-extract)](https://pypi.org/project/xyz17711-url-extract/)
[![License](https://img.shields.io/pypi/l/xyz17711-url-extract)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **url-extract-service**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[url-extract]"
```

## Methods

| Method | Description |
| --- | --- |
| `get_company_profile` | [Deprecated - use company_profile_get_profile] Company profile from a domain or a name as valid JSON ($0.009, x402) |
| `get_structured_data` | URL extract with a question: ask any web page a question and get structured data as JSON that matches your schema ($0.02, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`aget_company_profile` next to `get_company_profile`), sharing one underlying client.

## Quickstart

```python
from xyz17711_url_extract import Client

client = Client("https://api.17711.xyz/registry/url-extract-service")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-url-extract[langchain]"
```

```python
from xyz17711_url_extract import Client
from xyz17711_url_extract.langchain_tools import UrlExtractToolkit

client = Client("https://api.17711.xyz/registry/url-extract-service")
tools = UrlExtractToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
