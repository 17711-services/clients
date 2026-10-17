# xyz17711-domain-security

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-domain-security)](https://pypi.org/project/xyz17711-domain-security/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-domain-security)](https://pypi.org/project/xyz17711-domain-security/)
[![License](https://img.shields.io/pypi/l/xyz17711-domain-security)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **domain-security-service**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[domain-security]"
```

## Methods

| Method | Description |
| --- | --- |
| `get_report` | Domain security check: SSL certificate check, DMARC SPF check, DNSSEC, security headers and blocklist status with a score ($0.009, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`aget_report` next to `get_report`), sharing one underlying client.

## Quickstart

```python
from xyz17711_domain_security import Client

client = Client()  # talks to https://api.17711.xyz/registry/domain-security-service by default
# see the Methods table above for every available call and its request/response model
```

Pass another base URL (self-hosted instance, test server) as the first argument:
`Client("https://my-host.example/registry/domain-security-service")`.

## LangChain

```bash
pip install "xyz17711-domain-security[langchain]"
```

```python
from xyz17711_domain_security import Client
from xyz17711_domain_security.langchain_tools import DomainSecurityToolkit

client = Client()
tools = DomainSecurityToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
