from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from account.models import ROLES

STATUS = (
    ("PENDING", "PENDING"),
    ("REJECTED", "REJECTED"),
    ("APPROVED", "APPROVED"),
    ("CANCELED", "CANCELED"),
)


ROLES = (
    ("MANAGER", "MANAGER"),
    # ("INSPECTOR", "INSPECTOR"),
    ("SAFETY", "SAFETY"),
)


class AssessmentApproval(models.Model):
    assessment = models.ForeignKey(
        "assessment.Assessment", on_delete=models.CASCADE, related_name="approvals"
    )
    status = models.CharField(default="PENDING", choices=STATUS, max_length=20)
    by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    approver = models.CharField(default="SUPERVISOR", max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return f"{self.assessment} - {self.approver} - {self.assessment.job_test.id}"


class FirePreventionApproval(models.Model):
    fire_prevention = models.ForeignKey(
        "she.FirePrevention", on_delete=models.CASCADE, related_name="approvals"
    )
    status = models.CharField(default="PENDING", choices=STATUS, max_length=20)
    by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    approver = models.CharField(choices=ROLES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return f"{self.fire_prevention.shift.name} - {self.approver} - {self.fire_prevention.created_at.date()}"
