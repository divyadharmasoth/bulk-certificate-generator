from pathlib import Path
import re
import uuid

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_certificate(
    recipient_name: str,
    event_name: str,
    event_date: str,
    job_id: int
):
    # Create a separate folder for each generation job
    output_directory = (
        Path("generated_certificates")
        / f"job_{job_id}"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # Create a safe and unique filename
    safe_name = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        recipient_name
    ).strip("_")

    if not safe_name:
        safe_name = "certificate"

    unique_id = uuid.uuid4().hex[:8]

    file_path = (
        output_directory
        / f"{safe_name}_{unique_id}.pdf"
    )

    # Create PDF certificate
    pdf = canvas.Canvas(
        str(file_path),
        pagesize=A4
    )

    width, height = A4

    # Certificate title
    pdf.setFont(
        "Helvetica-Bold",
        28
    )

    pdf.drawCentredString(
        width / 2,
        height - 150,
        "CERTIFICATE OF PARTICIPATION"
    )

    # Main text
    pdf.setFont(
        "Helvetica",
        16
    )

    pdf.drawCentredString(
        width / 2,
        height - 230,
        "This is to certify that"
    )

    # Recipient name
    pdf.setFont(
        "Helvetica-Bold",
        24
    )

    pdf.drawCentredString(
        width / 2,
        height - 280,
        recipient_name
    )

    # Event information
    pdf.setFont(
        "Helvetica",
        16
    )

    pdf.drawCentredString(
        width / 2,
        height - 340,
        "has successfully participated in"
    )

    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawCentredString(
        width / 2,
        height - 390,
        event_name
    )

    # Event date
    pdf.setFont(
        "Helvetica",
        14
    )

    pdf.drawCentredString(
        width / 2,
        height - 450,
        f"Date: {event_date}"
    )

    # Signature line
    pdf.line(
        width / 2 - 60,
        150,
        width / 2 + 60,
        150
    )

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawCentredString(
        width / 2,
        130,
        "Authorized Signature"
    )

    # Save PDF
    pdf.save()

    return str(file_path)