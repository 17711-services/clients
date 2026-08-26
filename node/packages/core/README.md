# @xyz17711/core

[![npm](https://img.shields.io/npm/v/@xyz17711/core)](https://www.npmjs.com/package/@xyz17711/core)
[![License](https://img.shields.io/npm/l/@xyz17711/core)](https://github.com/17711-services/clients/blob/main/LICENSE)

Core HTTP client (transport, standardized error envelope) for the
[17711.xyz](https://api.17711.xyz) microservice fleet. Not meant to be used directly -- install a
specific service's own package instead, which depends on this one automatically:

```bash
npm install @xyz17711/ping
```

**No x402 payment support yet** (unlike `xyz17711_core` on the Python side) -- a gated tool
beyond its free quota surfaces as a plain `PlatformError` (HTTP 402), never signed/retried
automatically. Use the Python client if you need automatic payment today.

See the [Node.js section of the repo's own root README](https://github.com/17711-services/clients#nodejs)
for the current state of this client family.

## License

MIT -- see [`LICENSE`](../../LICENSE), shared by every language's client library in this repo.
