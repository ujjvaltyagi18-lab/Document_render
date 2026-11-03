
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from model import FormRequest, FormCreate
from pdf_service import generate_pdf
from pdf_reader import read_generated_pdf, write_generated_pdf

import os
import json
from pathlib import Path


app = FastAPI(title="ServiceHub Form Service")


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "forms.json"
PDF_FOLDER = BASE_DIR / "generated_forms"


# Load forms from JSON
def load_forms():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    return []


# Save forms into JSON
def save_forms():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(forms_data, file, indent=4)


# Load data at startup
forms_data = load_forms()


# Find form by ID
def find_form(form_id: int):
    return next(
        (item for item in forms_data if item["id"] == form_id),
        None
    )


# Generate unique ID
def generate_form_id():
    return max(
        (item["id"] for item in forms_data),
        default=0
    ) + 1


# Debug API
@app.get("/forms")
def get_forms():
    return {
        "total_forms": len(forms_data),
        "forms": forms_data,
        "json_file": str(DATA_FILE)
    }


# Create Form
@app.post("/send-form", response_model=FormRequest, status_code=201)
def create_form(data: FormCreate):

    form_id = generate_form_id()

    pdf_path = generate_pdf(
        form_id=form_id,
        name=data.name,
        item=data.item,
        options=data.options,
        dependent_name=data.dependent_name,
        dependent_age=data.dependent_age
    )

    response = {
        "id": form_id,
        "name": data.name,
        "email": str(data.email),
        "phone": data.phone,
        "item": data.item,
        "options": data.options,
        "dependent_name": data.dependent_name,
        "dependent_age": data.dependent_age,
        "pdf_path": str(pdf_path)
    }

    forms_data.append(response)
    save_forms()

    return response


# Download PDF
@app.get("/download-pdf/{form_id}")
def download_pdf(form_id: int):

    form = find_form(form_id)

    if not form:
        raise HTTPException(404, "Form not found")

    pdf_path = form["pdf_path"]

    if not os.path.exists(pdf_path):
        raise HTTPException(404, "PDF file not found")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"form_{form_id}.pdf"
    )


# Read any PDF
@app.get("/read-pdf")
def read_pdf(pdf_path: str):

    try:
        return read_generated_pdf(pdf_path)

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


class PDFWriteRequest(BaseModel):
    input_path: str
    text: str
    page_number: int = 0
    x: float = 100
    y: float = 100



# Read any PDF
from uuid import uuid4

@app.post("/write-pdf")
def write_pdf(data: PDFWriteRequest):
    try:
        PDF_FOLDER.mkdir(parents=True, exist_ok=True)

        output_path = PDF_FOLDER / f"updated_{uuid4().hex[:8]}.pdf"

        result = write_generated_pdf(
            input_path=data.input_path,
            output_path=str(output_path),
            text=data.text,
            page_number=data.page_number,
            x=data.x,
            y=data.y
        )

        return FileResponse(
            path=result,
            media_type="application/pdf",
            filename=output_path.name
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))