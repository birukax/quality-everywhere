from django.db import models
from django.contrib.auth.models import User as auth_user

REPORT_LIST = (
    ("FIRST-OFF", "FIRST-OFF"),
    ("ON-PROCESS", "ON-PROCESS"),
)


class ReportHeader(models.Model):
    report = models.CharField(max_length=20, choices=REPORT_LIST)
    no = models.CharField(max_length=30)
    machine = models.ForeignKey(
        "machine.Machine",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="report_header",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    by = models.ForeignKey(auth_user, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        if self.machine:
            return f"{self.no} - {self.machine.name}"
        else:
            return f"{self.no}"

    class Meta:
        ordering = ["no"]
        unique_together = ("report", "machine")
