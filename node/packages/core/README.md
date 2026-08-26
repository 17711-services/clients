# @xyz17711/core

[![Publish](https://github.com/17711-services/clients/actions/workflows/publish-node.yml/badge.svg)](https://github.com/17711-services/clients/actions/workflows/publish-node.yml)
[![npm](https://img.shields.io/npm/v/@xyz17711/core)](https://www.npmjs.com/package/@xyz17711/core)
[![License](https://img.shields.io/npm/l/@xyz17711/core)](https://github.com/17711-services/clients/blob/main/LICENSE)

Core HTTP client (transport, x402 payment, standardized error envelope) for the
[17711.xyz](https://api.17711.xyz) microservice fleet. Not meant to be used directly -- install a
specific service's own package instead, which depends on this one automatically:

```bash
npm install @xyz17711/ping
```

See the [Node family README](https://github.com/17711-services/clients/blob/main/node/README.md)
for the full guide: payment configuration (`x402PrivateKey` and friends), LangChain.js
integration, and error handling -- all of it lives in this package (`Client`, exported from every
generated service package too) and is shared by every generated service package.

## License

MIT -- see [`LICENSE`](../../LICENSE), shared by every language's client library in this repo.
