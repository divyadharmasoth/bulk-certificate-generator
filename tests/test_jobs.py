from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_test_job():
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
    return response.json()


def test_create_job():
    data = create_test_job()

    assert "job_id" in data
    assert data["total_recipients"] == 1
    assert data["completed"] == 1
    assert data["failed"] == 0
    assert data["status"] == "COMPLETED"


def test_get_job():
    job = create_test_job()
    job_id = job["job_id"]

    response = client.get(f"/api/jobs/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == job_id
    assert data["status"] == "COMPLETED"
    assert data["total_recipients"] == 1
    assert data["completed"] == 1
    assert data["failed"] == 0


def test_get_job_certificates():
    job = create_test_job()
    job_id = job["job_id"]

    response = client.get(
        f"/api/jobs/{job_id}/certificates"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == job_id
    assert "certificates" in data
    assert len(data["certificates"]) == 1

    certificate = data["certificates"][0]

    assert certificate["recipient_name"] == "Test User"
    assert certificate["recipient_email"] == "testuser@gmail.com"
    assert certificate["status"] == "SUCCESS"


def test_get_job_not_found():
    response = client.get("/api/jobs/999999")

    assert response.status_code == 404


def test_get_certificates_for_nonexistent_job():
    response = client.get(
        "/api/jobs/999999/certificates"
    )

    assert response.status_code == 404