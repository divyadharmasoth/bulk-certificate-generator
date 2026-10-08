from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job, Certificate
from app.schemas import GenerationRequest
from app.services.certificate_generator import generate_certificate


router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"]
)


@router.post("/")
def create_job(
    request: GenerationRequest,
    db: Session = Depends(get_db)
):
    # Create a new job
    job = Job(
        event_name=request.event_name,
        event_date=request.event_date,
        status="PROCESSING",
        total_count=len(request.recipients),
        completed_count=0,
        failed_count=0
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Process each recipient
    for recipient in request.recipients:

        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="PENDING"
        )

        db.add(certificate)
        db.commit()
        db.refresh(certificate)

        try:
            # Generate the PDF certificate
            file_path = generate_certificate(
                recipient_name=recipient.name,
                event_name=request.event_name,
                event_date=request.event_date,
                job_id=job.id
            )

            # Mark certificate as successful
            certificate.status = "SUCCESS"
            certificate.file_path = file_path

            job.completed_count += 1

        except Exception as error:
            # If one certificate fails, continue with the others
            certificate.status = "FAILED"
            certificate.error_message = str(error)

            job.failed_count += 1

        db.commit()

    # Update final job status
    if job.failed_count == 0:
        job.status = "COMPLETED"
    elif job.completed_count > 0:
        job.status = "COMPLETED_WITH_ERRORS"
    else:
        job.status = "FAILED"

    db.commit()

    return {
        "job_id": job.id,
        "status": job.status,
        "total_recipients": job.total_count,
        "completed": job.completed_count,
        "failed": job.failed_count
    }
@router.get("/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {
            "error": "Job not found"
        }

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "event_date": job.event_date,
        "status": job.status,
        "total_recipients": job.total_count,
        "completed": job.completed_count,
        "failed": job.failed_count
    }
@router.get("/{job_id}/certificates")
def get_job_certificates(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {
            "error": "Job not found"
        }

    certificates = (
        db.query(Certificate)
        .filter(Certificate.job_id == job_id)
        .all()
    )

    return {
        "job_id": job_id,
        "certificates": [
            {
                "certificate_id": certificate.id,
                "recipient_name": certificate.recipient_name,
                "recipient_email": certificate.recipient_email,
                "status": certificate.status,
                "file_path": certificate.file_path,
                "error_message": certificate.error_message
            }
            for certificate in certificates
        ]
    }
@router.get("/certificates/{certificate_id}")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = (
        db.query(Certificate)
        .filter(Certificate.id == certificate_id)
        .first()
    )

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if certificate.status != "SUCCESS":
        raise HTTPException(
            status_code=400,
            detail="Certificate was not generated successfully"
        )

    if not certificate.file_path:
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found"
        )

    return FileResponse(
        path=certificate.file_path,
        media_type="application/pdf",
        filename=f"{certificate.recipient_name.replace(' ', '_')}.pdf"
    )