import os
import reportlab
import time
from django.conf import settings
from io import BytesIO
from django.shortcuts import render
from django.http import FileResponse
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.lib.units import mm, inch
from assessment.models import Test
from reportlab.lib import colors, pdfencrypt
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Frame,
    PageTemplate,
    NextPageTemplate,
    PageBreak,
    Table,
    TableStyle,
    Preformatted,
    ListFlowable,
    ListItem,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.sequencer import getSequencer
from .tasks import FirstOff

# from .eob_flow import EOB


def test(request):

    response = FileResponse(
        generate_pdf(),
        as_attachment=True,
        filename="test.pdf",
    )

    return response


def generate_pdf():
    buffer = BytesIO()
    first_off = FirstOff(buffer)
    first_off.create()
    buffer.seek(0)
    return buffer
