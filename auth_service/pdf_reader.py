
from pathlib import Path
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError
from reportlab.pdfgen import canvas


def read_generated_pdf(pdf_path: str):

    file_path = Path(pdf_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if file_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported")

    try:
        reader = PdfReader(str(file_path))

        if reader.is_encrypted:
            raise ValueError("Encrypted PDF is not supported")

        result = {
            "file_name": file_path.name,
            "total_pages": len(reader.pages),
            "content": []
        }

        for index, page in enumerate(reader.pages):
            result["content"].append({
                "page": index + 1,
                "text": page.extract_text() or ""
            })

        return result

    except PdfReadError as e:
        raise ValueError(f"Invalid PDF file: {e}")


def write_generated_pdf(
    input_path: str,
    output_path: str,
    text: str,
    page_number: int = 0,
    x: float = 100,
    y: float = 100,
    font_size: int = 12
):

    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.is_file():
        raise FileNotFoundError(f"PDF not found: {input_path}")

    if input_file.suffix.lower() != ".pdf":
        raise ValueError("Input file must be a PDF")

    if output_file.suffix.lower() != ".pdf":
        raise ValueError("Output file must be a PDF")

    if input_file.resolve() == output_file.resolve():
        raise ValueError("Input and output files must be different")

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    if font_size <= 0:
        raise ValueError("Font size must be greater than zero")

    try:
        reader = PdfReader(str(input_file))

        if reader.is_encrypted:
            raise ValueError("Encrypted PDF is not supported")

        if not 0 <= page_number < len(reader.pages):
            raise ValueError("Invalid page number")

        page = reader.pages[page_number]

        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        if not (0 <= x < width and 0 <= y < height):
            raise ValueError("Coordinates are outside the PDF page")

        # Check horizontal text boundary
        from reportlab.pdfbase.pdfmetrics import stringWidth

        text_width = stringWidth(text, "Helvetica", font_size)

        if x + text_width > width:
            raise ValueError("Text exceeds the page width")

        packet = BytesIO()

        pdf = canvas.Canvas(packet, pagesize=(width, height))
        pdf.setFont("Helvetica", font_size)
        pdf.drawString(x, y, text)
        pdf.save()

        packet.seek(0)

        overlay_reader = PdfReader(packet)
        page.merge_page(overlay_reader.pages[0])

        writer = PdfWriter()

        for original_page in reader.pages:
            writer.add_page(original_page)

        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "wb") as file:
            writer.write(file)

        return str(output_file)

    except PdfReadError as e:
        raise ValueError(f"Unable to read PDF: {e}")
