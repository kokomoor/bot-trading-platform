from fastapi.testclient import TestClient

from app.services.api.main import app
from app.services.shared.platform_state import platform_state


def test_admin_endpoints_smoke() -> None:
    platform_state.strategies["s1"] = {"name": "S1"}
    client = TestClient(app)

    assert client.get("/admin/strategies").status_code == 200
    assert client.get("/admin/events").status_code == 200
    assert client.get("/admin/events/replay").status_code == 200


def test_kill_switch_toggle_endpoint() -> None:
    client = TestClient(app)

    enabled_response = client.post("/admin/kill-switch/true")
    assert enabled_response.status_code == 200
    assert enabled_response.json()["enabled"] is True

    disabled_response = client.post("/admin/kill-switch/false")
    assert disabled_response.status_code == 200
    assert disabled_response.json()["enabled"] is False


def test_adapter_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/admin/adapter-health")
    assert response.status_code == 200
    payload = response.json()
    assert "adapters" in payload


def test_health_degraded_flag() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] in {"ok", "degraded"}
