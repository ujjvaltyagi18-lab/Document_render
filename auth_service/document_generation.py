from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os


class DocumentGenerationExecutor:

    def execute(
        self,
        form_id: int,
        name: str,
        email: str,
        phone: str,
        item: str,
        options: list,
        dependent_name: str | None = None,
        dependent_age: int | None = None
    ):

        folder = "generated_forms"

       
        os.makedirs(folder, exist_ok=True)

        pdf_path = os.path.join(
            folder,
            f"form_{form_id}.pdf"
        )

        pdf = canvas.Canvas(
            pdf_path,
            pagesize=letter
        )

        pdf.setTitle(
            f"ServiceHub Form {form_id}"
        )

        y = 750

        pdf.drawString(
            100,
            y,
            "ServiceHub Fillable Form"
        )

        y -= 40

        pdf.drawString(
            100,
            y,
            f"Form ID : {form_id}"
        )

        y -= 30

        pdf.drawString(
            100,
            y,
            f"Name : {name}"
        )

        y -= 30

        pdf.drawString(
            100,
            y,
            f"Email : {email}"
        )

        y -= 30

        pdf.drawString(
            100,
            y,
            f"Phone : {phone}"
        )

        y -= 30

        pdf.drawString(
            100,
            y,
            f"Selected Item : {item}"
        )

        y -= 30

        pdf.drawString(
            100,
            y,
            "Options:"
        )

        y -= 20

        for option in options:
            pdf.drawString(
                120,
                y,
                f"- {option}"
            )
            y -= 20


        if dependent_name:

            y -= 20

            pdf.drawString(
                100,
                y,
                f"Dependent Name : {dependent_name}"
            )

            y -= 30

            pdf.drawString(
                100,
                y,
                f"Dependent Age : {dependent_age}"
            )


        pdf.save()

        return pdf_path