import pytest
from fastapi.testclient import TestClient
from starlette.middleware.cors import CORSMiddleware

from prodapi import ProdAPI


def test_that_fastapi_cant_be_imported_from_lib():
    with pytest.raises(ImportError):
        from prodapi import FastAPI  # noqa


def test_default_app_title():
    app = ProdAPI()
    assert app.title == "ProdAPI"


def test_invalid_http_path_prefix():
    with pytest.raises(
        RuntimeError, match="`http_path_prefix` must not end with a slash"
    ):
        ProdAPI(http_path_prefix="/ends-with-a-slash/")


def test_explicit_app_title():
    app = ProdAPI(title="My API")
    assert app.title == "My API"


def test_that_cors_middleware_can_be_added():
    app = ProdAPI().with_basic_cors()
    (cors_middleware,) = app.user_middleware
    assert cors_middleware.cls is CORSMiddleware


def test_that_health_routes_can_be_added():
    app = ProdAPI().with_health_routes()
    c = TestClient(app)
    resp = c.get("/__is-alive")
    assert resp.status_code == 200

    resp2 = c.get("/__is-ready")
    assert resp2.status_code == 200
