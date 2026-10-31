from pypdf import PdfReader


def read_generated_pdf(pdf_path: str):

    reader = PdfReader(pdf_path)

    result = {
        "total_pages": len(reader.pages),
        "content": []
    }

    for index, page in enumerate(reader.pages):

        text = page.extract_text()

        result["content"].append(
            {
                "page": index + 1,
                "text": text
            }
        )

        # Condition checking
        if text:

            if "Choice 1" in text:
                print("Choice 1 found")

            if "Ujjwal" in text:
                print("Name found")

    return result