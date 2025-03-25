from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from main.tasks import get_page, role_check
from django.http import FileResponse
from job.models import JobTest
from assessment.models import Assessment
from .models import ReportHeader
from she.models import FirePrevention, Incident
from report.reports.assessment import FirstOffReport, OnProcessReport
from report.reports.fire_prevention import FirePreventionReport
from report.reports.incident import IncidentReport
from .forms import CreateReportHeaderForm, EditReportHeaderForm


@login_required
def header_list(request):
    headers = ReportHeader.objects.all()

    page = get_page(request, model=headers)

    context = {
        "page": page,
    }
    return render(request, "report/header/list.html", context)


@login_required
def create_header(request):
    if request.method == "POST":
        form = CreateReportHeaderForm(request.POST)
        if form.is_valid():
            header = form.save(commit=False)
            header.by = request.user
            header.save()
            return redirect("report:header_list")
    else:
        form = CreateReportHeaderForm()
    context = {
        "form": form,
    }
    return render(request, "report/header/create.html", context)


@login_required
def edit_header(request, id):
    header = get_object_or_404(ReportHeader, id=id)
    if request.method == "POST":
        form = EditReportHeaderForm(request.POST, instance=header)
        if form.is_valid():
            header = form.save(commit=False)
            header.by = request.user
            header.save()
            return redirect("report:header_list")
    else:
        form = EditReportHeaderForm(instance=header)
    context = {
        "form": form,
        "header": header,
    }
    return render(request, "report/header/edit.html", context)


def get_assessment_report(request, id):

    buffer = BytesIO()
    elements = []
    job_test = get_object_or_404(JobTest, id=id)
    assessments = Assessment.objects.filter(job_test=job_test).order_by(
        "route_no", "type", "date", "time"
    )
    for assessment in assessments:
        if assessment.report_header == None:
            return redirect("job:test_detail", id=id)
        if assessment.type == "FIRST-OFF":
            first_off = FirstOffReport(
                buffer=buffer,
                elements=elements,
                assessment=assessment,
                id=id,
            )
            first_off.create()
        elif assessment.type == "ON-PROCESS":
            on_process = OnProcessReport(
                buffer=buffer,
                elements=elements,
                assessment=assessment,
                id=id,
            )
            on_process.create()
    first_off.save()
    buffer.seek(0)
    response = FileResponse(
        buffer,
        content_type="application/pdf",
        as_attachment=True,
        filename=f"{job_test.job.no}-{job_test.no}-{job_test.job.product.name}.pdf",
    )

    return response


def get_fire_prevention_report(request, id):
    buffer = BytesIO()
    elements = []
    fire_prevention = get_object_or_404(FirePrevention, id=id)
    report_header = ReportHeader.objects.filter(report="FIRE-PREVENTION").order_by(
        "-created_at"
    )
    if report_header.exists():
        fire_prevention_report = FirePreventionReport(
            buffer=buffer,
            elements=elements,
            report_header=report_header,
            id=id,
        )
        fire_prevention_report.create()
        fire_prevention_report.save()
    else:
        return redirect("she:fire_prevention_detail", id=id)
    buffer.seek(0)
    response = FileResponse(
        buffer,
        content_type="application/pdf",
        as_attachment=True,
        filename=f"fire-prevention-{fire_prevention.shift.name}-{fire_prevention.created_at.date().strftime("%d-%m-%Y")}.pdf",
    )
    return response


def get_incident_report(reqeust, id):
    buffer = BytesIO()
    elements = []
    incident = get_object_or_404(Incident, id=id)
    report_header = ReportHeader.objects.filter(report="INCIDENT").order_by(
        "-created_at"
    )
    if report_header.exists():
        incident_report = IncidentReport(
            buffer=buffer,
            elements=elements,
            report_header=report_header,
            id=id,
        )
        incident_report.create()
        incident_report.save()
    else:
        return redirect("she:incident_detail", id=id)
    buffer.seek(0)
    response = FileResponse(
        buffer,
        content_type="application/pdf",
        as_attachment=True,
        filename=f"incident-{incident.employee.name}-{incident.date.strftime("%d-%m-%Y")}.pdf",
    )
    return response
