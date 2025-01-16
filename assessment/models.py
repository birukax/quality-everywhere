import django
from django.db import models
import datetime
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
    TYPE = (
        ("FIRST-OFF", "FIRST-OFF"),
        ("ON-PROCESS", "ON-PROCESS"),
    )
    job_test = models.ForeignKey("job.JobTest", on_delete=models.CASCADE)
    type = models.CharField(
        max_length=20,
        choices=TYPE,
        null=True,
        blank=True,
    )
    date = models.DateField(default=datetime.datetime.today)
    time = models.TimeField(default=datetime.datetime.now)
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
        if self.type == "FIRST-OFF":
            return reverse("assessment:first_off_detail", args={self.id})
        elif self.type == "ON-PROCESS":
            return reverse("assessment:on_process_detail", args={self.id})

    def __str__(self):
        return f"{self.job_test.job} - {self.machine}"


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
    )
    time = models.TimeField(default=datetime.datetime.now)
    sample_no = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )
    action = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.assessment.machine} - {self.conformity}"
