import django
from django.db import models
from datetime import date, time, datetime
from django.contrib.auth.models import User
from django.urls import reverse
import django.utils
import django.utils.timezone


class Assessment(models.Model):
    STATUS = (
        ("OPEN", "OPEN"),
        ("PENDING", "PENDING"),
        ("REJECTED", "REJECTED"),
        ("COMPLETED", "COMPLETED"),
    )
    job_test = models.ForeignKey("job.JobTest", on_delete=models.CASCADE)
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
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="OPEN",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    inspected_by = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="inspected_assessments",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("assessment:detail", args={self.id})

    def __str__(self):
        return f"{self.job} - {self.no} - {self.machine}"


class Test(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # type = models.CharField(max_length=100)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Conformity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # type = models.CharField(max_length=100)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "conformities"

    def __str__(self):
        return self.name


class FirstOff(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="first_offs",
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    value = models.BooleanField(null=True, blank=True)
    remark = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.assessment.machine} - {self.test}"


class OnProcess(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="on_processes",
    )
    conformity = models.ForeignKey(
        Conformity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date = models.DateField(default=django.utils.timezone.now)
    time = models.TimeField(default=django.utils.timezone.now)
    action = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.assessment.machine} - {self.conformity}"
