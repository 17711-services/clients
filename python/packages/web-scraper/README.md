# xyz17711-web-scraper

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-web-scraper)](https://pypi.org/project/xyz17711-web-scraper/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-web-scraper)](https://pypi.org/project/xyz17711-web-scraper/)
[![License](https://img.shields.io/pypi/l/xyz17711-web-scraper)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **web-scraper**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[web-scraper]"
```

## Methods

| Method | Description |
| --- | --- |
| `extract_markdown` | URL to Markdown: read any web page and get its main article content as clean Markdown for agents ($0.003, x402) |
| `get_task_status` | Polls for the result of a task enqueued by a *_async tool |
| `scrape_url` | Scrape URL: fetch any web page through a proxy and get its status, content type and raw HTML ($0.002, x402) |
| `scrape_url_async` | [Deprecated - use web_scraper_scrape_url] Enqueues a web_scraper_scrape_url job and returns a task id immediately ($0.002, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`aextract_markdown` next to `extract_markdown`), sharing one underlying client.

## Quickstart

```python
from xyz17711_web_scraper import Client

client = Client("https://api.17711.xyz/registry/web-scraper")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-web-scraper[langchain]"
```

```python
from xyz17711_web_scraper import Client
from xyz17711_web_scraper.langchain_tools import WebScraperToolkit

client = Client("https://api.17711.xyz/registry/web-scraper")
tools = WebScraperToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
