from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from model import DocumentRequest
from document_generation import DocumentGenerationExecutor

router = APIRouter()

executor = DocumentGenerationExecutor()


@router.post("/generate")
def generate_document(request: DocumentRequest):

    pdf = executor.execute(request.model_dump())

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=document.pdf"
        },
    )