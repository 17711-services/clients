# xyz17711-extract-correct

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-extract-correct)](https://pypi.org/project/xyz17711-extract-correct/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-extract-correct)](https://pypi.org/project/xyz17711-extract-correct/)
[![License](https://img.shields.io/pypi/l/xyz17711-extract-correct)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **extract-correct-service**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[extract-correct]"
```

## Methods

| Method | Description |
| --- | --- |
| `parse_json` | JSON repair API: extract valid JSON from messy text or model output and fix it against a JSON Schema ($0.006, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`aparse_json` next to `parse_json`), sharing one underlying client.

## Quickstart

```python
from xyz17711_extract_correct import Client

client = Client("https://api.17711.xyz/registry/extract-correct-service")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-extract-correct[langchain]"
```

```python
from xyz17711_extract_correct import Client
from xyz17711_extract_correct.langchain_tools import ExtractCorrectToolkit

client = Client("https://api.17711.xyz/registry/extract-correct-service")
tools = ExtractCorrectToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
