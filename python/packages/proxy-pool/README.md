# xyz17711-proxy-pool

[![PyPI](https://img.shields.io/pypi/v/xyz17711-proxy-pool)](https://pypi.org/project/xyz17711-proxy-pool/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-proxy-pool)](https://pypi.org/project/xyz17711-proxy-pool/)
[![License](https://img.shields.io/pypi/l/xyz17711-proxy-pool)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **proxy-pool**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[proxy-pool]"
```

## Methods

| Method | Description |
| --- | --- |
| `get_best_proxy` | Returns one of the fastest verified-alive proxies matching the filter, randomized to spread load ($0.001, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`aget_best_proxy` next to `get_best_proxy`), sharing one underlying client.

## Quickstart

```python
from xyz17711_proxy_pool import Client

client = Client("https://api.17711.xyz/registry/proxy-pool")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-proxy-pool[langchain]"
```

```python
from xyz17711_proxy_pool import Client
from xyz17711_proxy_pool.langchain_tools import ProxyPoolToolkit

client = Client("https://api.17711.xyz/registry/proxy-pool")
tools = ProxyPoolToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
