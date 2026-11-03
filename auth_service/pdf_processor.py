
import os
from pypdf import PdfReader


class PDFProcessor:

    def read_pdf(self, pdf_path: str) -> dict:
        """
        Read PDF and extract text from all pages.
        """

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        reader = PdfReader(pdf_path)

        if reader.is_encrypted:
            raise ValueError("Encrypted PDF is not supported")

        result = {
            "total_pages": len(reader.pages),
            "content": []
        }

        for index, page in enumerate(reader.pages):

            text = page.extract_text() or ""

            result["content"].append({
                "page": index + 1,
                "text": text
            })

        return result

    def get_form_fields(self, pdf_path: str) -> dict:
        """
        Get PDF form field information.
        """

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        reader = PdfReader(pdf_path)

        if reader.is_encrypted:
            raise ValueError("Encrypted PDF is not supported")

        fields = reader.get_fields() or {}

        return {
            "total_fields": len(fields),
            "fields": {
                name: {
                    "type": str(field.get("/FT", "")),
                    "value": str(field.get("/V", ""))
                }
                for name, field in fields.items()
            }
        }
