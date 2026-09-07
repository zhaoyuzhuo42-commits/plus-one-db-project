import pytest
import json
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


#get events
def test_get_all_events_returns_200(client):
    response = client.get("/api/events")
    assert response.status_code == 200

def test_get_all_events_get_events(client):
    response = client.get("/api/events")
    body = response.json()
    assert "events" in body

def test_get_all_events_get_all_events(client):
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


#get event_id
def test_get_event_id_returns_200(client):
    reponse = client.get("/api/events/1")
    assert reponse.status_code == 200

def test_get_event_id_returns_correct_event(client):
    with open ("db/data/events.json") as f:
        seed_events = json.load(f)
    reponse = client.get("/api/events/1")
    result = reponse.json()["event"]
    assert result["id"] == 1
    assert result["title"] == seed_events[0]["title"]


def test_get_event_id_not_found_returns_404(client):
    reponse = client.get("/api/events/999")
    assert reponse.status_code == 404

def test_get_event_id_not_intger_returns_400(client):
    response = client.get("/api/events/hello")
    assert response.status_code == 400

#POST /api/auth/login

def test_login_return_200_with_valid_credentials(client):
    reponse = client.post("/api/suth/login",
                          json={ 
                              "email": "alice@example.com",
                              "password": "password123"}
                              )
    assert reponse.status_code == 200
    result = reponse.json()
    assert "token" in result

def test_login_email_not_found_return_401(client):
    reponse = client.post("/api/suth/login",
                              json={ 
                                  "email": "notfound@example.com",
                                  "password": "password123"}
                                  )
    assert reponse.status_code == 401

def test_login_password_incorrect_return_401(client):
    reponse = client.post("/api/suth/login",
                              json={ 
                                  "email": "alice@example.com",
                                  "password": "passwordincorrect"}
                                  )
    assert reponse.status_code == 401

def test_login_missing_email_return_400(client):
    reponse = client.post("/api/suth/login",
                              json={ 
                                  "password": "password123"}
                                  )
    assert reponse.status_code == 400

def test_login_missing_password_return_400(client):
    reponse = client.post("/api/suth/login",
                          json={ 
                              "email": "alice@example.com"}
                              )
    assert reponse.status_code == 400