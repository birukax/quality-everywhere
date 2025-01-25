from django.shortcuts import render, get_object_or_404, redirect
from assessment.models import Assessment
from .models import AssessmentApproval


def approvals(request):
    context = {}
    assessments = AssessmentApproval.objects.filter(status="PENDING")
    context["assessments"] = assessments
    return render(request, "approval/list.html", context)


def create_assessment_approval(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    if assessment.type == "FIRST-OFF":
        if not assessment.status in ("PENDING", "COMPLETED"):
            approvers = ["OPERATOR", "SUPERVISOR"]
            for a in approvers:
                app = AssessmentApproval(assessment=assessment, approver=a)
                app.save()
            assessment.status = "PENDING"
            assessment.inspected_by = request.user
            assessment.save()
        return redirect("assessment:first_off_detail", id=assessment.id)
    return redirect("assessment:on_process_detail", id=assessment.id)


def assessment_list(request, type):

    assessments = AssessmentApproval.objects.filter(
        status="PENDING", assessment__type=type
    )
    context = {"assessments": assessments}
    return render(request, "approval/assessment/list.html", context)


def approve_assessment(request, id):
    assessment = get_object_or_404(AssessmentApproval, id=id)
    assessment.status = "APPROVED"
    assessment.by = request.user
    assessment.save()
    not_approved = AssessmentApproval.objects.filter(
        assessment__id=assessment.assessment.id, status="PENDING"
    )
    if not not_approved.exists():
        assessment.assessment.status = "COMPLETED"
        assessment.assessment.save()
        type = assessment.assessment.type
        if type == "FIRST-OFF":
            assessment.assessment.job_test.status = "FIRST-OFF COMPLETED"
            assessment.assessment.job_test.save()
        # elif type == "ON-PROCESS":
        #     assessment.assessment.job_test.status = "ON-PROCESS COMPLETED"
        #     assessment.assessment.job_test.save()
        assessment.assessment.job_test.save()
    return redirect("approval:assessment_list", type=assessment.assessment.type)


def reject_assessment(request, id):
    assessment = get_object_or_404(AssessmentApproval, id=id)
    assessment.status = "REJECTED"
    assessment.by = request.user
    assessment.save()
    not_approved = AssessmentApproval.objects.filter(
        assessment__id=assessment.assessment.id, status="PENDING"
    )
    if not_approved.exists():
        for a in not_approved:
            a.status = "CANCELED"
            a.by = request.user
            a.save()
    assessment.assessment.status = "REJECTED"
    assessment.assessment.save()
    return redirect("approval:assessment_list", type=assessment.assessment.type)
