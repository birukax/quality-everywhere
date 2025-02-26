from django.shortcuts import render, get_object_or_404, redirect
from assessment.models import Assessment
from .models import AssessmentApproval
from .filters import AssessmentApprovalFilter
from main.tasks import get_page


def approvals(request):
    context = {}
    assessments = AssessmentApproval.objects.filter(status="PENDING")
    context["assessments"] = assessments
    return render(request, "approval/list.html", context)


def create_assessment_approval(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    if assessment.type == "FIRST-OFF":
        if not assessment.status in ("PENDING", "COMPLETED"):
            # approvers = ["OPERATOR", "SUPERVISOR"]
            # for a in approvers:
            app = AssessmentApproval(assessment=assessment)
            app.save()
            assessment.status = "PENDING"
            assessment.inspected_by = request.user
            assessment.save()
    return redirect("assessment:first_off_detail", id=assessment.id)


def assessment_list(request, type):

    apps = AssessmentApproval.objects.filter(status="PENDING", assessment__type=type)
    assessment_approval_filter = AssessmentApprovalFilter(request.GET, queryset=apps)
    apps = assessment_approval_filter.qs
    page = get_page(request, model=apps)

    context = {
        "page": page,
        "filter": assessment_approval_filter,
    }
    return render(request, "approval/assessment/list.html", context)


def approve_assessment(request, id):
    app = get_object_or_404(AssessmentApproval, id=id)
    app.status = "APPROVED"
    app.by = request.user
    app.save()
    # not_approved = AssessmentApproval.objects.filter(
    #     assessment__id=app.assessment.id, status="PENDING"
    # )
    # if not not_approved.exists():
    app.assessment.status = "COMPLETED"
    type = app.assessment.type
    if type == "FIRST-OFF" and not app.assessment.extra:
        app.assessment.job_test.status = "FIRST-OFF COMPLETED"
        app.assessment.job_test.save()
    app.assessment.save()
    # elif type == "ON-PROCESS":
    #     app.assessment.job_test.status = "ON-PROCESS COMPLETED"
    #     app.assessment.job_test.save()
    # app.assessment.job_test.save()
    return redirect("approval:assessment_list", type=app.assessment.type)


def reject_assessment(request, id):
    app = get_object_or_404(AssessmentApproval, id=id)
    app.status = "REJECTED"
    app.by = request.user
    app.save()
    # not_approved = AssessmentApproval.objects.filter(
    #     assessment__id=app.assessment.id, status="PENDING"
    # )
    # if not_approved.exists():
    # for a in not_approved:
    #     a.status = "CANCELED"
    #     a.by = request.user
    #     a.save()
    app.assessment.status = "REJECTED"
    app.assessment.save()
    return redirect("approval:assessment_list", type=app.assessment.type)
