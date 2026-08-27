import pytest
import json
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)

def test_get_all_events_returns_200(client):
    response = client.get("/api/events")
    assert response.status_code == 200

def test_get_all_events_get_events(client):
    response = client.get("/api/events")
    body = response.json()
    assert "events" in body

def test_get_all_events_get_events(client):
    response = client.get("/api/events")
    with open ("db/data/events.json") as f:
        seeded_events =  json.load(f)
        seeded_title = [event["title"]
                        for event in seeded_events]
    results = response.json()["events"]
    result_title = [result["title"]
                    for result in results]
    assert len(seeded_events) == len(results)
    assert sorted(seeded_title) == sorted(result_title)