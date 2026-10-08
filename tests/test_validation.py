from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_invalid_email():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Test Workshop",
            "event_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "invalid-email"
                }
            ]
        }
    )

    assert response.status_code == 422


def test_missing_email():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Test Workshop",
            "event_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Test User"
                }
            ]
        }
    )

    assert response.status_code == 422


def test_empty_recipients():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Test Workshop",
            "event_date": "2026-10-08",
            "recipients": []
        }
    )

    assert response.status_code == 422