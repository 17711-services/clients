# clients

Typed client libraries for the [17711.xyz](https://api.17711.xyz) microservice fleet -- pay-per-call
APIs settled in USDC via the [x402](https://x402.org) protocol, listed on
[x402scan](https://www.x402scan.com/server/f1c7b972-3405-4b75-8b4f-d1bfbd6305ff). One repo, one directory per language -- everything here is
generated directly from each service's own live OpenAPI document, never hand-written.

## Python

[`python/`](python/) -- `pip install "xyz17711[ping]"`. See
[`python/README.md`](python/README.md) for the full guide.

## Node.js

[`node/`](node/) -- `npm install @xyz17711/ping`. See [`node/README.md`](node/README.md) for the
full guide, or a package's own README for one specific service.

## License

MIT -- see [`LICENSE`](LICENSE), shared by every language's client library in this repo.
