# xyz17711-emoji-match

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-python.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-python.yml)
[![PyPI](https://img.shields.io/pypi/v/xyz17711-emoji-match)](https://pypi.org/project/xyz17711-emoji-match/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711-emoji-match)](https://pypi.org/project/xyz17711-emoji-match/)
[![License](https://img.shields.io/pypi/l/xyz17711-emoji-match)](https://github.com/17711-services/clients/blob/main/LICENSE)

Typed Python client for **emoji-match-service**, part of the
[17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call APIs settled in USDC via
[x402](https://x402.org), listed on [x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). See the
[Python family README](https://github.com/17711-services/clients/blob/main/python/README.md)
for the full guide (payment configuration, LangChain integration, logging, error handling) -- this
page only covers what's specific to this one package.

## Install

```bash
pip install "xyz17711[emoji-match]"
```

## Methods

| Method | Description |
| --- | --- |
| `suggest_emojis` | Emoji suggestion API: text in 18 languages in, the 1 to 5 best matching emoji out, deterministic and fast ($0.002, x402) |

Every method above has both a sync form and an async form (the `a`-prefixed sibling, e.g.
`asuggest_emojis` next to `suggest_emojis`), sharing one underlying client.

## Quickstart

```python
from xyz17711_emoji_match import Client

client = Client("https://api.17711.xyz/registry/emoji-match-service")
# see the Methods table above for every available call and its request/response model
```

## LangChain

```bash
pip install "xyz17711-emoji-match[langchain]"
```

```python
from xyz17711_emoji_match import Client
from xyz17711_emoji_match.langchain_tools import EmojiMatchToolkit

client = Client("https://api.17711.xyz/registry/emoji-match-service")
tools = EmojiMatchToolkit(client=client).get_tools()
```

## License

MIT -- see the repository's own `LICENSE`.
