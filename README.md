# prodapi

[![Continuous Integration Status](https://github.com/jmagnusson/prodapi/actions/workflows/ci.yml/badge.svg)](https://github.com/jmagnusson/prodapi/actions/workflows/ci.yml)
[![Continuous Delivery Status](https://github.com/jmagnusson/prodapi/actions/workflows/cd.yml/badge.svg)](https://github.com/jmagnusson/prodapi/actions/workflows/cd.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/prodapi.svg)](https://pypi.org/project/prodapi/)
[![Code Coverage](https://img.shields.io/codecov/c/github/jmagnusson/prodapi?color=%2334D058)](https://codecov.io/gh/jmagnusson/prodapi)
[![PyPI Package](https://img.shields.io/pypi/v/prodapi?color=%2334D058&label=pypi%20package)](https://pypi.org/project/prodapi)

A thin layer on top of [FastAPI](https://fastapi.tiangolo.com/) with the following features:

- Integrates with [FastAPI-Security](https://jmagnusson.github.io/fastapi-security/) to add a custom route `/users/me` (path is overridable)
- Easily add CORS to your app by calling `app.with_basic_cors()`
- Add health routes to the app via `app.with_health_routes()`. Adds a liveness route at `/__is-alive` and a readiness route at `/__is-ready` (both paths can be overridden). Useful together with [Kubernetes liveness and readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) for example.
- And, thanks to FastAPI, all routes are automatically added to the API documentation

## Installation

```
pip install prodapi
```

## Example

```python
from prodapi import ProdAPI, ApiRouter, FastAPISecurity

# First let's set up security, via FastAPI-Security

security = FastAPISecurity()

# Set up HTTP Basic Auth
security.init_basic_auth([
    {"username": "johndoe", "password": "123"},
    {"username": "janedoe", "password": "abc123"},
])

# Set up OAuth2 and OIDC
# NOTE: There is also `init_oauth2_through_jwks` in case OIDC is not available
security.init_oauth2_through_oidc(
    "https://my-auth0-tenant.eu.auth0.com/.well-known/openid-configuration",
)

# Make sure that basic auth user `jane` and OAuth2 user
# `p56OnzZb8KrWC9paxCyv8ylyB2flTIky@clients` gets all permissions automatically.
# NOTE: For basic auth you have to set up permissions this way, for OAuth2 permissions
#       will be automatically extracted from the incoming JWT token (via the key
#       `permissions`, which might only be implemented for Auth0)
security.add_permission_overrides({
    "jane": ["*"],
    "p56OnzZb8KrWC9paxCyv8ylyB2flTIky@clients": ["*"],
)

# Now we're ready to create the app
# NOTE: ProdAPI is just a thin layer on top of `fastapi.FastAPI`
app = ProdAPI()

# CORS - Allow any origins, methods and headers. Don't expose any headers.
app.with_basic_cors()

# Add routes `/__is-alive` and `/__is-ready`. Useful together with Kubernetes or similar
# URL paths are configurable.
app.with_health_routes()

# Enable `/users/me` route to get info about the user. URL path is configurable.
app.with_user_routes(security)

# Create our app specific API router and our routes
products_router = ApiRouter()

@products_router.get("/products")
def list_products():
    return []

app.include_router(products_router)

# And we're done! Now just use uvicorn or similar to deploy.

```

## TODO
1. Create cli utility (using [tiangolo typer](https://github.com/tiangolo/typer)?), which can generate:
    1. A stub project using `prodapi`
    1. Frontend (React?)
    1. docker-compose.yml and Dockerfile
    1. Kubernetes deployment files
