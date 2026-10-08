from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    event_name = Column(String, nullable=False)
    event_date = Column(String, nullable=False)

    status = Column(String, default="PENDING")

    total_count = Column(Integer, default=0)
    completed_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    recipient_name = Column(String, nullable=False)
    recipient_email = Column(String, nullable=False)

    status = Column(String, default="PENDING")

    file_path = Column(String, nullable=True)
    error_message = Column(String, nullable=True)