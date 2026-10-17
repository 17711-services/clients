# xyz17711-ip-blocklist

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-ip-blocklist)](https://pypi.org/project/xyz17711-ip-blocklist/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-ip-blocklist)](https://pypi.org/project/xyz17711-ip-blocklist/)
[![License](https://img.shields.io/pypi/l/xyz17711-ip-blocklist)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **ip-blocklist**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[ip-blocklist]"
```

## Methods

| Method | Description |
| --- | --- |
| `check_ip` | IP reputation check: is this IPv4 address on a public threat blocklist (Tor exit nodes, botnets, spam networks) ($0.010, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`acheck_ip` next to `check_ip`), sharing one underlying client.

## Quickstart

```python
from xyz17711_ip_blocklist import Client

client = Client("https://api.17711.xyz/registry/ip-blocklist")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-ip-blocklist[langchain]"
```

```python
from xyz17711_ip_blocklist import Client
from xyz17711_ip_blocklist.langchain_tools import IpBlocklistToolkit

client = Client("https://api.17711.xyz/registry/ip-blocklist")
tools = IpBlocklistToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
