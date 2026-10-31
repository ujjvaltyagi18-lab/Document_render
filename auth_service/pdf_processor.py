from io import BytesIO
from typing import Any, Optional

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    NameObject,
    BooleanObject,
)


class PDFDocumentExecutor:


    def set_need_appearances(
        self,
        writer: PdfWriter
    ):
        """
        Enable PDF viewer to generate field appearances
        """

        if "/AcroForm" not in writer._root_object:

            writer._root_object.update(
                {
                    NameObject("/AcroForm"):
                    writer._add_object({})
                }
            )

        acro_form = writer._root_object["/AcroForm"]

        acro_form.update(
            {
                NameObject("/NeedAppearances"):
                BooleanObject(True)
            }
        )


    def update_field(
        self,
        annotation,
        field_name: str,
        data: dict
    ):

        """
        Update PDF field value
        """

        if field_name in data:

            annotation.update(
                {
                    NameObject("/V"):
                    str(data[field_name]),

                    NameObject("/Ff"):
                    1
                }
            )


    def execute(
        self,
        input_path: str,
        output_pdf_path: str,
        data: Any
    ) -> Optional[bytes]:


        try:

            pdf_reader = PdfReader(
                input_path
            )

            pdf_writer = PdfWriter()


            self.set_need_appearances(
                pdf_writer
            )


            for page in pdf_reader.pages:


                if "/Annots" in page:


                    for annotation_ref in page["/Annots"]:


                        annotation = (
                            annotation_ref.get_object()
                        )


                        if "/T" in annotation:


                            field_name = str(
                                annotation["/T"]
                            )


                            print(
                                "PDF Field:",
                                field_name
                            )


                            self.update_field(
                                annotation,
                                field_name,
                                data
                            )


                pdf_writer.add_page(
                    page
                )


            # Save output PDF

            with open(
                output_pdf_path,
                "wb"
            ) as file:

                pdf_writer.write(
                    file
                )


            # Return PDF bytes

            pdf_buffer = BytesIO()

            pdf_writer.write(
                pdf_buffer
            )


            print(
                "Generated PDF saved:",
                output_pdf_path
            )


            return pdf_buffer.getvalue()


        except Exception as e:

            print(
                f"Failed to process PDF: {e}"
            )

            return None