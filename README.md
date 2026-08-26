# clients

Typed client libraries for the [17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call
APIs settled in USDC via the [x402](https://x402.org) protocol, listed on
[x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). One repo, one directory per language -- everything here is
generated directly from each service's own live OpenAPI document, never hand-written.

## Python

[`python/`](python/) -- `pip install "xyz17711[ping]"`. See
[`python/README.md`](python/README.md) for the full guide.

## Node.js

Coming soon -- npm scope will be `@xyz17711`. Not published yet (the existing generator/packages
predate the payment/LangChain/generated-tests overhaul the Python client already has); use the
Python client above in the meantime.

## License

MIT -- see [`LICENSE`](LICENSE), shared by every language's client library in this repo.
