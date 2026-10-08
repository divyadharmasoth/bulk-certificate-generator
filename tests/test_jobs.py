from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_create_job():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Test Python Workshop",
            "event_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "testuser@gmail.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["total_recipients"] == 1
    assert data["completed"] == 1
    assert data["failed"] == 0


def test_get_job():
    response = client.get("/api/jobs/2")

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == 2
    assert "status" in data
    assert "total_recipients" in data


def test_get_job_certificates():
    response = client.get("/api/jobs/2/certificates")

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == 2
    assert "certificates" in data
    assert len(data["certificates"]) >= 1