from fastapi.testclient import TestClient
from {{project_slug}} import app


def test_health_is_ready():
    client = TestClient(app)
    resp = client.get("/__is-ready")
    assert resp.status_code == 200
