import os

from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

FOLDER = "generated_forms"

HEADING = Color(0.31, 0.42, 0.66)   # blue used for headings in the sample PDF
ITEMS = ["Choice 1", "Choice 2", "Choice 3", "Choice 4"]
OPTIONS = ["Option 1", "Option 2", "Option 3"]


def generate_pdf(
    form_id,
    name,
    item="Choice 1",
    options=None,
    dependent_name=None,
    dependent_age=None,
):
    """Builds the 'Sample Fillable PDF' (name field, dropdown, 3 checkboxes,
    dependent table) pre-filled with the submitted values. Returns the file path."""

    options = options or []
    os.makedirs(FOLDER, exist_ok=True)
    file_path = os.path.join(FOLDER, f"form_{form_id}.pdf")

    pdf = canvas.Canvas(file_path, pagesize=letter)
    pdf.setTitle("Sample Fillable PDF")
    form = pdf.acroForm

    # ---- title + intro
    pdf.setFillColor(HEADING)
    pdf.setFont("Helvetica", 17)
    pdf.drawString(74, 694, "Sample Fillable PDF")

    pdf.setFillColor(black)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(
        74, 668,
        "This is an example of a fillable PDF. A client can save it and email it back to you, or print it and",
    )
    pdf.drawString(74, 650, "bring it along with them to a meeting with you.")

    # ---- name
    pdf.setFillColor(HEADING)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(74, 616, "Please enter your name:")
    form.textfield(
    name="Name",
    value=name or "",
    tooltip="Name",
    x=202.5,
    y=588,
    width=210,
    height=22,
    borderWidth=0,
    fillColor=white,
    forceBorder=False,
    fontSize=11,
    fieldFlags="readOnly",
)

    # ---- dropdown
    pdf.setFillColor(HEADING)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(
        74, 564,
        "Please select an item from the combo/dropdown list:"
    )

    pdf.setFillColor(black)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(74, 548, "First Choice")

    selected_item = item if item in ITEMS else ITEMS[0]

    form.choice(
        name="Dropdown2",
        value=selected_item,
        tooltip="Dropdown",
        options=ITEMS,
        x=71.7,
        y=524.8,
        width=150,
        height=20,
        borderWidth=0,
        fillColor=white,
        forceBorder=False,
        fieldFlags="combo readOnly",
        fontSize=11,
    )

    # ---- checkboxes
    pdf.setFillColor(HEADING)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(74, 503, "Check all that apply:")

    y = 479.3

    for option in OPTIONS:
        form.checkbox(
            name=option,
            tooltip=option,
            checked=option in options,
            x=73.2,
            y=y,
            size=13,
            buttonStyle="check",
            borderWidth=1,
            borderColor=black,
            fillColor=white,
            textColor=black,
            forceBorder=True,
            fieldFlags="readOnly",
        )

        pdf.setFillColor(black)
        pdf.setFont("Helvetica", 11)
        pdf.drawString(89, y + 3, option)

        y -= 14.6

    # ---- dependent table
    pdf.setFillColor(HEADING)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(74, 424, "You can add  fields within tables as well:")

    left, mid, right = 68, 183, 425
    top, row, bottom = 416.5, 401, 386
    pdf.setStrokeColor(black)
    pdf.setLineWidth(0.8)
    pdf.rect(left, bottom - 0.5, right - left, top - bottom + 0.5)
    pdf.line(left, row, right, row)
    pdf.line(mid, bottom - 0.5, mid, top)

    pdf.setFillColor(black)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(74, 405, "Name of Dependent")
    pdf.drawString(74, 390, "Age of Dependent")

    form.textfield(
    name="Name of Dependent",
    value=dependent_name or "",
    tooltip="Name of Dependent",
    x=183.6,
    y=401.3,
    width=232.4,
    height=14,
    borderWidth=0,
    fillColor=white,
    forceBorder=False,
    fontSize=9,
    fieldFlags="readOnly",
)
    form.textfield(
    name="Age of Dependent",
    value="" if dependent_age is None else str(dependent_age),
    tooltip="Age of Dependent",
    x=183.6,
    y=386.2,
    width=232.4,
    height=14,
    borderWidth=0,
    fillColor=white,
    forceBorder=False,
    fontSize=9,
    fieldFlags="readOnly",
)

    pdf.save()
    return file_path