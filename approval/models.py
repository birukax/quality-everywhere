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


class FirstOffApproval(models.Model):
    quality_test = models.ForeignKey(
        "quality_test.QualityTest", on_delete=models.CASCADE
    )
    status = models.CharField(default="PENDING", choices=STATUS, max_length=20)
    by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    approver = models.CharField(choices=ROLES, max_length=20)
    # approved_at = models.DateTimeField(auto_now_add=True)s
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.quality_test} - {self.approver}"
