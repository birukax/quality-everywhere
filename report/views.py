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
from job.models import JobTest
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.sequencer import getSequencer
from .tasks import FirstOff, OnProcess

# from .eob_flow import EOB


def get_report(request, id):
    response = FileResponse(
        generate_pdf(id),
        as_attachment=True,
        filename="test.pdf",
    )

    return response


def generate_pdf(id):
    buffer = BytesIO()
    # first_off = FirstOff(buffer=buffer, id=id)
    # first_off.create()
    on_process = OnProcess(buffer=buffer, id=id)
    on_process.create()
    buffer.seek(0)
    return buffer
