# Bulk Certificate Generator

A backend API for generating personalized certificates in bulk from a single request.

This project was developed for the Backend Assignment — Bulk Certificate Generator. It accepts a certificate generation request containing event information and multiple recipients, validates the input, generates an individual PDF certificate for each recipient using a predefined template, stores job and certificate information in a relational database, tracks success and failure status, and provides APIs to inspect jobs and retrieve generated certificates.

## Assignment Requirements Covered

The implementation covers the required functionality specified in the assignment:

- Accept a certificate generation request
- Accept multiple recipients in a single request
- Validate recipient data
- Generate a certificate for each valid recipient
- Use a single predefined certificate template
- Include recipient-specific information in generated certificates
- Track job and individual certificate status
- Continue processing other recipients if one certificate generation fails
- Report successful and failed certificate generations
- Allow clients to check job status/progress/result
- Allow generated certificates to be retrieved
- Use a relational database
- Include automated tests for important application flows
- Provide setup, execution, testing, API usage, and design documentation

## Features

- Bulk certificate generation
- Personalized PDF certificates
- FastAPI REST API
- Pydantic input validation
- SQLAlchemy ORM
- SQLite relational database
- Job-level status tracking
- Individual certificate status tracking
- Successful/failed certificate counts
- Per-certificate error messages
- Failure isolation — one failed certificate does not stop the remaining recipients
- Certificate file storage
- Certificate download endpoint
- Swagger/OpenAPI interactive documentation
- Automated Pytest test suite
- Synchronous bulk processing with documented design reasoning

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
├── main.py
├── requirements.txt
├── README.md
└── .gitignore