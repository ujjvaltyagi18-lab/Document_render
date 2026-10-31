
import os
from itertools import count
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from model import FormCreate
from pdf_service import generate_pdf


pdf_ids = count(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("generated_forms", exist_ok=True)
    yield


app = FastAPI(
    title="ServiceHub Form Service",
    lifespan=lifespan
)


# Create form and generate PDF
@app.post("/send-form", status_code=201)
def create_form(data: FormCreate):
    form_id = next(pdf_ids)

    try:
        pdf_path = generate_pdf(
            form_id,
            data.name,
            data.item,
            data.options,
            data.dependent_name,
            data.dependent_age
        )

        return {
            "message": "Form submitted and PDF generated successfully",
            "form_id": form_id,
            "name": data.name,
            "email": str(data.email),
            "phone": data.phone,
            "item": data.item,
            "options": data.options,
            "dependent_name": data.dependent_name,
            "dependent_age": data.dependent_age,
            "pdf_path": str(pdf_path)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {str(e)}"
        )


# Download PDF by ID
@app.get("/forms/{form_id}/pdf")
def download_pdf(form_id: int):
    pdf_path = os.path.join(
        "generated_forms",
        f"form_{form_id}.pdf"
    )

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404,
            detail="PDF file not found"
        )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"form_{form_id}.pdf"
    )
