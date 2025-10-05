from fastapi.testclient import TestClient

from src.api.main import app


def test_metrics_endpoint():
    client = TestClient(app)
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "scrape_runs_total" in response.text
