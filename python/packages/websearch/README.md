# xyz17711-websearch

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-websearch)](https://pypi.org/project/xyz17711-websearch/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-websearch)](https://pypi.org/project/xyz17711-websearch/)
[![License](https://img.shields.io/pypi/l/xyz17711-websearch)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **websearch**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[websearch]"
```

## Methods

| Method | Description |
| --- | --- |
| `get_task_status` | Polls for the result of a task enqueued by a *_async tool |
| `search_web` | Web search API for agents: search the web and get result titles, URLs and snippets as JSON ($0.005, x402) |
| `search_web_async` | [Deprecated - use websearch_search_web] Enqueues a websearch_search_web job and returns a task id immediately ($0.005, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`aget_task_status` next to `get_task_status`), sharing one underlying client.

## Quickstart

```python
from xyz17711_websearch import Client

client = Client()  # talks to https://api.17711.xyz/registry/websearch by default
# see the Methods table above for every available call and its request/response model
```

Pass another base URL (self-hosted instance, test server) as the first argument:
`Client("https://my-host.example/registry/websearch")`.

## LangChain

```bash
pip install "xyz17711-websearch[langchain]"
```

```python
from xyz17711_websearch import Client
from xyz17711_websearch.langchain_tools import WebsearchToolkit

client = Client()
tools = WebsearchToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
