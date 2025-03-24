from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from main.tasks import get_page, role_check
from django.http import FileResponse
from job.models import JobTest
from assessment.models import Assessment
from report.reports.assessment import FirstOff, OnProcess
from .models import ReportHeader
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
    response = FileResponse(
        buffer,
        content_type="application/pdf",
        as_attachment=True,
        filename=f"{job_test.job.no}-{job_test.no}-{job_test.job.product.name}.pdf",
    )

    return response
