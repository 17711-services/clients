# xyz17711-contact-finder

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-contact-finder)](https://pypi.org/project/xyz17711-contact-finder/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-contact-finder)](https://pypi.org/project/xyz17711-contact-finder/)
[![License](https://img.shields.io/pypi/l/xyz17711-contact-finder)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **contact-finder-service**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[contact-finder]"
```

## Methods

| Method | Description |
| --- | --- |
| `get_contacts` | Contact finder: public business emails, phone numbers, contact forms and support pages of a domain, with role and source ($0.009, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`aget_contacts` next to `get_contacts`), sharing one underlying client.

## Quickstart

```python
from xyz17711_contact_finder import Client

client = Client("https://api.17711.xyz/registry/contact-finder-service")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-contact-finder[langchain]"
```

```python
from xyz17711_contact_finder import Client
from xyz17711_contact_finder.langchain_tools import ContactFinderToolkit

client = Client("https://api.17711.xyz/registry/contact-finder-service")
tools = ContactFinderToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
