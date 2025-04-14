from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from assessment.models import Assessment
from she.models import FirePrevention
from she.forms import SubmitFPChecklistForm
from .models import AssessmentApproval, FirePreventionApproval, ROLES
from .filters import AssessmentApprovalFilter
from main.tasks import get_page, role_check


@login_required
@role_check(["ADMIN", "SHIFT-SUPERVISOR"])
def approvals(request):
    context = {}
    assessments = AssessmentApproval.objects.filter(status="PENDING")
    context["assessments"] = assessments
    return render(request, "approval/list.html", context)


@login_required
@role_check(["ADMIN", "INSPECTOR", "SUPERVISOR"])
def create_assessment_approval(request, id):
    assessment = get_object_or_404(Assessment, id=id)
    if assessment.type == "FIRST-OFF":
        if not assessment.status in ["PENDING", "COMPLETED"]:
            # approvers = ["OPERATOR", "SUPERVISOR"]
            # for a in approvers:
            app = AssessmentApproval(assessment=assessment)
            app.save()
            assessment.status = "PENDING"
            assessment.inspected_by = request.user
            assessment.save()
    return redirect("assessment:first_off_detail", id=assessment.id)


@login_required
@role_check(["ADMIN", "SHIFT-SUPERVISOR"])
def assessment_list(request, type):
    apps = AssessmentApproval.objects.select_related("assessment").filter(
        status="PENDING", assessment__type=type
    )
    assessment_approval_filter = AssessmentApprovalFilter(request.GET, queryset=apps)
    apps = assessment_approval_filter.qs
    page = get_page(request, model=apps)

    context = {
        "page": page,
        "filter": assessment_approval_filter,
    }
    return render(request, "approval/assessment/list.html", context)


@login_required
@role_check(["ADMIN", "SHIFT-SUPERVISOR", "MANAGER"])
def update_assessment_approval(request, id):
    if request.method == "POST":
        app = get_object_or_404(AssessmentApproval, id=id)
        if app.status == "PENDING":
            reason = request.POST.get("reason")
            action = request.POST.get("action")
            if action == "approve":
                app.status = "APPROVED"
                app.assessment.status = "COMPLETED"
                type = app.assessment.type
                if type == "FIRST-OFF" and not app.assessment.extra:
                    app.assessment.job_test.status = "FIRST-OFF COMPLETED"
                    app.assessment.job_test.save()
            elif action == "reject":
                app.status = "REJECTED"
                app.assessment.status = "REJECTED"
            else:
                return redirect("approval:assessment_list", type=app.assessment.type)
            app.by = request.user
            app.reason = reason
            app.approver = request.user.profile.role
            app.assessment.save()
            app.save()
    return redirect("approval:assessment_list", type=app.assessment.type)


# @login_required
# @role_check(["ADMIN", "SHIFT-SUPERVISOR"])
# def approve_assessment(request, id):
#     app = get_object_or_404(AssessmentApproval, id=id)
#     if app.status == "PENDING":
#         app.status = "APPROVED"
#         app.by = request.user
#         app.save()
#         # not_approved = AssessmentApproval.objects.filter(
#         #     assessment__id=app.assessment.id, status="PENDING"
#         # )
#         # if not not_approved.exists():
#         app.assessment.status = "COMPLETED"
#         type = app.assessment.type
#         if type == "FIRST-OFF" and not app.assessment.extra:
#             app.assessment.job_test.status = "FIRST-OFF COMPLETED"
#             app.assessment.job_test.save()
#         app.assessment.save()
#         # elif type == "ON-PROCESS":
#         #     app.assessment.job_test.status = "ON-PROCESS COMPLETED"
#         #     app.assessment.job_test.save()
#         # app.assessment.job_test.save()
#     return redirect("approval:assessment_list", type=app.assessment.type)


# @login_required
# @role_check(["ADMIN", "SHIFT-SUPERVISOR"])
# def reject_assessment(request, id):
#     app = get_object_or_404(AssessmentApproval, id=id)
#     if app.status == "PENDING":
#         app.status = "REJECTED"
#         app.by = request.user
#         app.save()
#         # not_approved = AssessmentApproval.objects.filter(
#         #     assessment__id=app.assessment.id, status="PENDING"
#         # )
#         # if not_approved.exists():
#         # for a in not_approved:
#         #     a.status = "CANCELED"
#         #     a.by = request.user
#         #     a.save()
#         app.assessment.status = "REJECTED"
#         app.assessment.save()
#     return redirect("approval:assessment_list", type=app.assessment.type)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER", "SUPERVISOR"])
def fire_prevention_list(request):
    apps = FirePreventionApproval.objects.filter(
        status="PENDING", approver=request.user.profile.role
    )
    page = get_page(request, model=apps)
    context = {
        "page": page,
    }
    return render(request, "approval/fire_prevention/list.html", context)


@login_required
def create_fire_prevention_approval(request, id):
    fire_prevention = get_object_or_404(FirePrevention, id=id)
    if request.method == "POST" and fire_prevention.status in ["OPEN", "REJECTED"]:
        form = SubmitFPChecklistForm(request.POST)
        if form.is_valid():
            fire_prevention.comment = form.cleaned_data["comment"]
            for r in ROLES:
                FirePreventionApproval.objects.create(
                    fire_prevention=fire_prevention, approver=r[0]
                )
            fire_prevention.status = "PENDING"
            fire_prevention.inspected_by = request.user
            fire_prevention.save()

    return redirect("she:fire_prevention_detail", id=fire_prevention.id)


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER"])
def approve_fire_prevention(request, id):
    fire_prevention_approval = get_object_or_404(FirePreventionApproval, id=id)
    fire_prevention = FirePrevention.objects.get(
        id=fire_prevention_approval.fire_prevention.id
    )
    fp_approvals = FirePreventionApproval.objects.filter(
        fire_prevention=fire_prevention
    )
    if fire_prevention.status == "PENDING" and (
        request.user.profile.role == fire_prevention_approval.approver
        or request.user.is_superuser
    ):
        fire_prevention_approval.status = "APPROVED"
        fire_prevention_approval.by = request.user
        fire_prevention_approval.save()
        pending_approvals = fp_approvals.filter(status="PENDING")
        if not pending_approvals.exists():
            fire_prevention.status = "COMPLETED"
            fire_prevention.save()
    return redirect("approval:fire_prevention_list")


@login_required
@role_check(["ADMIN", "SAFETY", "MANAGER"])
def reject_fire_prevention(request, id):
    fire_prevention_approval = get_object_or_404(FirePreventionApproval, id=id)
    fire_prevention = FirePrevention.objects.get(
        id=fire_prevention_approval.fire_prevention.id
    )
    fp_approvals = FirePreventionApproval.objects.filter(
        fire_prevention=fire_prevention
    )
    if fire_prevention.status == "PENDING" and (
        request.user.profile.role == fire_prevention_approval.approver
        or request.user.is_superuser
    ):
        fire_prevention_approval.status = "REJECTED"
        fire_prevention_approval.by = request.user
        fire_prevention_approval.save()
        pending_approvals = fp_approvals.filter(status="PENDING")
        if pending_approvals.exists():
            for pending in pending_approvals:
                pending.status = "CANCELED"
                pending.by = request.user
                pending.save()
        fire_prevention.status = "REJECTED"
        fire_prevention.save()
    return redirect("approval:fire_prevention_list")
