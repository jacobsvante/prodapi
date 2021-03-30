from fastapi.testclient import TestClient

from prodapi import ProdAPI


def test_that_is_alive_returns_expected_data():
    app = ProdAPI().with_health_routes()
    c = TestClient(app)
    resp = c.get("/__is-alive")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert data["version"] == "0.1.0"
    assert data["environment"] == "dev"
    assert data["message"] is None
    assert "node" in data


def test_that_is_ready_returns_expected_data():
    app = ProdAPI().with_health_routes()
    c = TestClient(app)
    resp = c.get("/__is-ready")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert data["version"] == "0.1.0"
    assert data["environment"] == "dev"
    assert data["message"] is None
    assert "node" in data


def test_that_readiness_can_return_503():
    msg = "Not ready because of database connectivity or something..."

    def fail():
        return msg

    app = ProdAPI().with_health_routes(ready_checks=[fail])
    c = TestClient(app)
    resp = c.get("/__is-ready")
    assert resp.status_code == 503
    data = resp.json()
    assert data["ok"] is False
    assert data["message"] == msg
