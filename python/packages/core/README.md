# xyz17711

[![PyPI](https://img.shields.io/pypi/v/xyz17711)](https://pypi.org/project/xyz17711/)
[![Python versions](https://img.shields.io/pypi/pyversions/xyz17711)](https://pypi.org/project/xyz17711/)
[![License](https://img.shields.io/pypi/l/xyz17711)](https://github.com/17711-services/python-clients/blob/main/LICENSE)

Core HTTP client (transport, x402 payment, standardized error envelope) for the
[17711.xyz](https://api.17711.xyz) microservice fleet. Not meant to be used directly -- install a
specific service's own package instead, which depends on this one automatically:

```bash
pip install "xyz17711[ping]"
```

See the [top-level README](https://github.com/17711-services/python-clients#readme) for the full
guide: payment configuration (`x402_private_key` and friends), LangChain integration, logging,
and error handling -- all of it lives in this package (`xyz17711_core.Client`) and is shared by
every generated service package.

## License

MIT -- see the repository's own `LICENSE`.
