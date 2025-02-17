from io import BytesIO
from django.shortcuts import render
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape, letter
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
    p = canvas.Canvas(buffer)

    tests = Test.objects.all()
    p.drawString(100, 750, "Test")

    y = 700
    for t in tests:
        p.drawString(100, y, f"Name: {t.name}")
        p.drawString(100, y - 20, f"Critical: {t.critical}")
        y -= 30
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
