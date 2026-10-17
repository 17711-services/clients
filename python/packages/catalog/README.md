# xyz17711-catalog

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-catalog)](https://pypi.org/project/xyz17711-catalog/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-catalog)](https://pypi.org/project/xyz17711-catalog/)
[![License](https://img.shields.io/pypi/l/xyz17711-catalog)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **catalog**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[catalog]"
```

## Methods

| Method | Description |
| --- | --- |
| `category` | Lists every registration in one category, paginated (public GET) |
| `find_services_by_capability` | Ranks registered services/tools by relevance to a free-text query |
| `search` | Ranks registered services/tools by relevance to a free-text query (public GET) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`acategory` next to `category`), sharing one underlying client.

## Quickstart

```python
from xyz17711_catalog import Client

client = Client()  # talks to https://api.17711.xyz/registry/catalog by default
# see the Methods table above for every available call and its request/response model
```

Pass another base URL (self-hosted instance, test server) as the first argument:
`Client("https://my-host.example/registry/catalog")`.

## LangChain

```bash
pip install "xyz17711-catalog[langchain]"
```

```python
from xyz17711_catalog import Client
from xyz17711_catalog.langchain_tools import CatalogToolkit

client = Client()
tools = CatalogToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
