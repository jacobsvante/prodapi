# ProdAPI

A thin layer on top of [FastAPI](https://fastapi.tiangolo.com/) to add some production readiness features.

## Key features

- Integrates with [FastAPI-Security](https://jmagnusson.github.io/fastapi-security/) to add a custom route `/users/me` (path is overridable)
- Easily add CORS to your app by calling `app.with_basic_cors()`
- Add health routes to the app via `app.with_health_routes()`. Adds a liveness route at `/__is-alive` and a readiness route at `/__is-ready` (both paths can be overridden). Useful together with [Kubernetes liveness and readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) for example.
- And, thanks to FastAPI, all routes are automatically added to the API documentation

## Installation

```
pip install prodapi
```

## Usage example

An example app using ProdAPI [can be found here](https://github.com/jmagnusson/prodapi/tree/main/examples).

## Developers

To run the tests, do:

1. Install Poetry (https://python-poetry.org/docs/)
1. Install dependencies `poetry install`
1. Run tests: `poetry run pytest`

Before committing and publishing a pull request, do:

1. Install pre-commit globally: `pip install pre-commit`
1. Run `pre-commit install` to install the Git hook

[pre-commit](https://pre-commit.com/) will ensure that all code is formatted per our conventions. Failing to run this will probably make the CI tests fail in the PR instead.
