from io import BytesIO
from django.shortcuts import render
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.lib.units import mm, inch
from assessment.models import Test


def test(request):

    response = FileResponse(
        generate_pdf(),
        as_attachment=True,
        filename="test.pdf",
    )

    return response


def generate_pdf():
    buffer = BytesIO()

    def string_alignment(c):
        width, height = A4

        c.drawString(80, 700, "Standard String")
        c.drawRightString(80, 680, "Right String")

        numbers = [987.15, 44, -1, 234.56, (456.78)]
        y = 650
        for number in numbers:
            c.drawAlignedString(80, y, str(number))
            y -= 20

        c.drawCentredString(width / 2, 550, "Centered String")

    def rotate_demo(c):
        c.translate(inch, inch)
        c.setFont("Helvetica", 14)
        c.drawString(inch, inch, "Normal")
        c.line(inch, inch, inch + 100, inch)

        c.rotate(45)
        c.drawString(inch, -inch, "45 Degrees")
        c.line(inch, inch, inch + 100, inch)

        c.rotate(45)
        c.drawString(inch, -inch, "90 Degrees")
        c.line(inch, inch, inch + 100, inch)

    def font_demo(c, fonts):
        pos_y = 350
        for font in fonts:
            c.setFont(font, 12)
            c.drawString(100, pos_y, font)
            pos_y -= 10

    def coord(x, y, height, unit=1):
        x, y = x * unit, y * unit
        return x, y

    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.drawString(
        *coord(width / 2, height / 2, inch),
        text=f"welcome to reportlab!{[*coord(width, height, inch)]}",
    )
    fonts = c.getAvailableFonts()
    font_demo(c, fonts)
    c.showPage()
    rotate_demo(c)
    c.showPage()
    string_alignment(c)
    c.showPage()

    c.save()

    buffer.seek(0)
    return buffer
