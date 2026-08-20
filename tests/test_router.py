import pytest
from fastapi.testclient import TestClient
from db.router import app

@pytest.fixture
def client():
    return TestClient(app)

def test_get_all_events_returns_200_and_seeded_events(client):
    response = client.get("/api/events")
    assert response.status_code == 200
    titles = [event["title"] for event in response.json()["events"]]
    assert "Leeds Tech Meetup – June Edition" in titles
