import pytest
from fastapi import Depends
from fastapi.security import HTTPBasicCredentials
from fastapi.testclient import TestClient
from fastapi_security.exceptions import AuthNotConfigured

from prodapi import FastAPISecurity, ProdAPI, User


def test_that_user_route_raise_exception_when_auth_is_not_configured():
    security = FastAPISecurity()
    app = ProdAPI().with_user_routes(security)
    c = TestClient(app)

    with pytest.raises(AuthNotConfigured):
        c.get("/users/me")


def test_that_user_route_works_with_auth_configured():
    cred = HTTPBasicCredentials(username="johndoe", password="123")
    security = FastAPISecurity()
    security.init_basic_auth([cred])
    app = ProdAPI().with_user_routes(security)

    with TestClient(app) as c:
        resp = c.get("/users/me")

        assert resp.status_code == 200
        data = resp.json()
        assert data["auth"]["auth_method"] == "none"

    with TestClient(app) as c:
        resp = c.get("/users/me", auth=("johndoe", "123"))

        assert resp.status_code == 200
        data = resp.json()
        assert data["auth"]["auth_method"] == "basic_auth"
        assert data["auth"]["subject"] == "johndoe"


def test_that_user_route_includes_user_permissions():
    cred = HTTPBasicCredentials(username="johndoe", password="123")
    security = FastAPISecurity()
    security.init_basic_auth([cred])
    security.add_permission_overrides({"johndoe": "*"})
    security.user_permission("products:create")
    security.user_permission("products:delete")

    app = ProdAPI().with_user_routes(security)

    with TestClient(app) as c:
        resp = c.get("/users/me")

        assert resp.status_code == 200
        data = resp.json()
        assert data["auth"]["auth_method"] == "none"

    with TestClient(app) as c:
        resp = c.get("/users/me", auth=("johndoe", "123"))
        data = resp.json()
        assert data["auth"]["permissions"] == ["products:create", "products:delete"]


def test_that_user_without_permission_is_denied_access():
    cred = HTTPBasicCredentials(username="johndoe", password="123")
    security = FastAPISecurity()
    security.init_basic_auth([cred])
    app = ProdAPI()

    create_product_perm = security.user_permission("products:create")

    @app.post("/products")
    def create_product(
        user: User = Depends(security.user_holding(create_product_perm)),
    ):
        return {}

    with TestClient(app) as c:
        resp = c.post("/products", auth=("johndoe", "123"))

        assert resp.status_code == 403
        assert resp.json() == {"detail": "Missing required permission products:create"}


def test_that_user_with_permission_is_granted_access():
    cred = HTTPBasicCredentials(username="johndoe", password="123")

    security = FastAPISecurity()
    security.init_basic_auth([cred])
    security.add_permission_overrides({"johndoe": ["products:create"]})
    app = ProdAPI()

    create_product_perm = security.user_permission("products:create")

    @app.post("/products")
    def create_product(
        user: User = Depends(security.user_holding(create_product_perm)),
    ):
        return {"ok": True}

    with TestClient(app) as c:
        resp = c.post("/products", auth=("johndoe", "123"))

        assert resp.status_code == 200
        assert resp.json() == {"ok": True}


def test_that_user_with_wildcard_permission_is_granted_access():
    cred = HTTPBasicCredentials(username="johndoe", password="123")

    security = FastAPISecurity()
    security.init_basic_auth([cred])
    security.add_permission_overrides({"johndoe": "*"})
    app = ProdAPI()

    create_product_perm = security.user_permission("products:create")

    @app.post("/products")
    def create_product(
        user: User = Depends(security.user_holding(create_product_perm)),
    ):
        return {"ok": True}

    with TestClient(app) as c:
        resp = c.post("/products", auth=("johndoe", "123"))

        assert resp.status_code == 200
        assert resp.json() == {"ok": True}
