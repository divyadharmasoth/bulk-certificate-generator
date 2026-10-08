from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_download_certificate():
    response = client.get("/api/jobs/certificates/3")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_certificate_not_found():
    response = client.get("/api/jobs/certificates/9999")

    assert response.status_code == 404


def test_job_certificates():
    response = client.get("/api/jobs/2/certificates")

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == 2
    assert len(data["certificates"]) >= 1

def test_individual_certificate_failure(monkeypatch):

    import app.routes.jobs as jobs_module

    original_generate_certificate = jobs_module.generate_certificate

    def mock_generate_certificate(
        recipient_name,
        event_name,
        event_date,
        job_id
    ):
        # Simulate a certificate generation failure
        # only for this particular recipient.
        if recipient_name == "Fail User":
            raise Exception("Simulated certificate generation failure")

        # Generate normally for other recipients.
        return original_generate_certificate(
            recipient_name=recipient_name,
            event_name=event_name,
            event_date=event_date,
            job_id=job_id
        )

    monkeypatch.setattr(
        jobs_module,
        "generate_certificate",
        mock_generate_certificate
    )

    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Failure Test Workshop",
            "event_date": "2026-10-08",
            "recipients": [
                {
                    "name": "Valid User",
                    "email": "valid@gmail.com"
                },
                {
                    "name": "Fail User",
                    "email": "fail@gmail.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_recipients"] == 2
    assert data["completed"] == 1
    assert data["failed"] == 1
    assert data["status"] == "COMPLETED_WITH_ERRORS"