from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class QualityTest(models.Model):
    STATUS = (
        ("OPEN", "OPEN"),
        ("PENDING", "PENDING"),
        ("REJECTED", "REJECTED"),
        ("COMPLETED", "COMPLETED"),
    )
    job = models.ForeignKey(
        "job.Job", on_delete=models.CASCADE, related_name="quality_tests"
    )
    no = models.IntegerField(default=1)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    shift = models.ForeignKey(
        "misc.Shift",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    machine = models.ForeignKey(
        "machine.Machine", on_delete=models.CASCADE, null=True, blank=True
    )
    paper = models.ForeignKey(
        "misc.Paper",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    batch_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="OPEN",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_quality_tests",
        blank=True,
        null=True,
    )
    inspected_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="inspected_quality_tests",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("quality_test:detail", args={self.id})

    def __str__(self):
        return f"{self.job} - {self.no} - {self.machine}"
