# Bulk Certificate Generator

A backend API for generating personalized certificates in bulk from a single request.

The system accepts an event name, event date, and a list of recipients. It validates the recipient data, generates an individual PDF certificate for each recipient using a predefined template, stores job and certificate information in a relational database, tracks generation status, and provides APIs to retrieve generated certificates.

## Features

- Bulk certificate generation
- Personalized PDF certificates
- Single predefined certificate template
- Recipient data validation
- SQLite relational database
- Job status tracking
- Individual certificate status tracking
- Successful and failed certificate tracking
- Failure isolation between recipients
- Certificate retrieval
- Certificate PDF download
- REST API using FastAPI
- Swagger API documentation
- Automated tests using Pytest

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab
- Pytest
- HTTPX
- Uvicorn

## Project Structure

```text
bulk-certificate-generator/
│
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   └── jobs.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── certificate_generator.py
│   │
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   ├── __init__.py
│   ├── test_jobs.py
│   ├── test_validation.py
│   └── test_certificates.py
│
├── generated_certificates/
├── certificates.db
├── main.py
├── README.md
└── .gitignore