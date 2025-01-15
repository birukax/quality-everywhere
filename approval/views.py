from django.shortcuts import render, get_object_or_404, redirect
from assessment.models import Assessment
from .models import FirstOffApproval


# def approvals(request):
#     return render(request, 'approval/list.html', context)


# def create_first_off_approval(request, id):
#     first_off = get_object_or_404(QualityTest, id=id)
#     if not first_off.status == "PENDING":
#         approvers = ["OPERATOR", "SUPERVISOR"]
#         for a in approvers:
#             app = FirstOffApproval(first_off=first_off, approver=a)
#             app.save()
#         first_off.status = "PENDING"
#         first_off.inspected_by = request.user
#         first_off.save()
#     return redirect("first_off:list", status="PENDING")


# def first_offs(request):

#     first_offs = FirstOffApproval.objects.filter(status="PENDING")
#     context = {"first_offs": first_offs}
#     return render(request, "approval/first_off/list.html", context)


# def approve_first_off(request, id):
#     first_off = get_object_or_404(FirstOffApproval, id=id)
#     first_off.status = "APPROVED"
#     first_off.by = request.user
#     first_off.save()
#     not_approved = FirstOffApproval.objects.filter(
#         first_off__id=first_off.first_off.id, status="PENDING"
#     )
#     if not not_approved.exists():
#         first_off.first_off.status = "COMPLETED"
#         first_off.first_off.save()

#     return redirect("approval:first_offs")


# def reject_first_off(request, id):
#     first_off = get_object_or_404(FirstOffApproval, id=id)
#     first_off.status = "REJECTED"
#     first_off.by = request.user
#     first_off.save()
#     not_approved = FirstOffApproval.objects.filter(
#         first_off__id=first_off.first_off.id, status="PENDING"
#     )
#     if not_approved.exists():
#         for a in not_approved:
#             a.status = "CANCELED"
#             a.by = request.user
#             a.save()
#     first_off.first_off.status = "REJECTED"
#     first_off.first_off.save()
#     return redirect("approval:first_offs")
