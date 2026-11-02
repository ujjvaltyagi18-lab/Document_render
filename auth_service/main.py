from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from model import FormRequest, FormCreate
from pdf_service import generate_pdf

import os


app = FastAPI(
    title="ServiceHub Form Service"
)


forms_data = []


@app.post("/send-form", response_model=FormRequest, status_code=201)
def create_form(data: FormCreate):

    form_id = len(forms_data) + 1

    # Generate PDF
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

        "email": data.email,

        "phone": data.phone,

        "item": data.item,

        "options": data.options,

        "dependent_name": data.dependent_name,

        "dependent_age": data.dependent_age,

        "pdf_path": pdf_path
    }


    forms_data.append(response)

    return response



# Only PDF Download API
@app.get("/download-pdf/{form_id}")
def download_pdf(form_id: int):

    form = next(
        (item for item in forms_data if item["id"] == form_id),
        None
    )


    if not form:
        raise HTTPException(
            status_code=404,
            detail="Form not found"
        )


    pdf_path = form["pdf_path"]


    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404,
            detail="PDF file not found"
        )


    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"form_{form_id}.pdf"
    )