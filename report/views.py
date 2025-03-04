import os
import reportlab
import time
from django.conf import settings
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
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
from assessment.models import Assessment
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
    elements = []
    job_test = get_object_or_404(JobTest, id=id)
    assessments = Assessment.objects.filter(job_test=job_test).order_by(
        "route_no", "date", "time"
    )
    for assessment in assessments:
        if assessment.type == "FIRST-OFF":
            first_off = FirstOff(
                buffer=buffer, elements=elements, assessment=assessment, id=id
            )
            first_off.create()
        elif assessment.type == "ON-PROCESS":
            on_process = OnProcess(
                buffer=buffer, elements=elements, assessment=assessment, id=id
            )
            on_process.create()
    first_off.save()
    buffer.seek(0)
    return buffer
