# ProdAPI

A thin layer on top of [FastAPI](https://fastapi.tiangolo.com/) to add some production readiness features.

## Key features

- Integrates with [FastAPI-Security](https://jmagnusson.github.io/fastapi-security/) to add a custom route `/users/me` (path is overridable)
- Easily add CORS to your app by calling `app.with_basic_cors()`
- Add health routes to the app via `app.with_health_routes()`. Adds a liveness route at `/__is-alive` and a readiness route at `/__is-ready` (both paths can be overridden). Useful together with [Kubernetes liveness and readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) for example.
- And, thanks to FastAPI, all routes are automatically added to the API documentation

Installation

```
pip install prodapi
```

## Usage example

An example app using ProdAPI [can be found here](https://github.com/jmagnusson/prodapi/tree/main/examples).
