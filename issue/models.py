import os
import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from main.validators import validate_image


def issue_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = (
        f"{instance.issue_type.name}-{instance.location.name}-{instance.id}.{ext}"
    )
    return os.path.join("issues/", new_filename)


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    @property
    def have_issues(self):
        return Issue.objects.filter(location=self).exclude(status="COMPLETED").exists()

    @property
    def active_issues(self):
        return Issue.objects.filter(location=self).exclude(status="COMPLETED").count()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Employee(models.Model):

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Terminated", "Terminated"),
    ]
    name = models.CharField(max_length=100)
    no = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.RESTRICT,
        related_name="employees",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")
    employment_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["name", "no"]

    def __str__(self):
        return self.name


class IssueType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Issue(models.Model):
    STATUS = (
        ("CREATED", "CREATED"),
        ("CANCELLED", "CANCELLED"),
        ("PENDING", "PENDING"),
        ("INCOMPLETE", "INCOMPLETE"),
        ("COMPLETED", "COMPLETED"),
        # ("ACCEPTED", "ACCEPTED"),
        # ("REJECTED", "REJECTED"),
        # ("IN-PROGRESS", "IN-PROGRESS"),
    )
    TYPE = (
        ("PRODUCTION", "PRODUCTION"),
        ("SAFETY", "SAFETY"),
    )

    issue_type = models.ForeignKey(
        IssueType, on_delete=models.RESTRICT, related_name="issues"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="CREATED",
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE,
        default="SAFETY",
    )
    location = models.ForeignKey(
        Location, on_delete=models.RESTRICT, related_name="issues"
    )
    department = models.ForeignKey(
        Department, on_delete=models.RESTRICT, related_name="issues"
    )
    observation = models.TextField(max_length=200)
    suggestion = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(
        upload_to=issue_image_upload_path,
        validators=[validate_image],
        help_text="Upload Image",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="issues"
    )

    def get_absolute_url(self):
        return reverse("issue:detail", args={self.id})

    def __str__(self):
        return f"{self.issue_type} - {self.location} - {self.status}"

    class Meta:
        ordering = ["created_at"]


class IncidentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"


class Incident(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, related_name="incidents"
    )
    location = models.ForeignKey(
        Location, on_delete=models.RESTRICT, related_name="incidents"
    )
    type = models.ForeignKey(
        IncidentType, on_delete=models.RESTRICT, related_name="incidents"
    )
    date = models.DateField(default=datetime.datetime.now)
    time = models.TimeField(default=datetime.datetime.now)
    witness_list = models.ManyToManyField(
        Employee,
        related_name="witnessed_incidents",
        blank=True,
    )
    referred_to_hospital = models.BooleanField(default=False)
    cause = models.TextField(max_length=200)
    body_part_injured = models.CharField(max_length=75)
    nature_of_injury = models.CharField(max_length=75)
    pre_incident_activity = models.TextField(max_length=100)
    tools_used_before_incident = models.TextField(max_length=100)
    recommendation = models.TextField(max_length=100)
    action_taken = models.TextField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="incidents"
    )

    class Meta:
        ordering = ["-date", "time"]

    def get_absolute_url(self):
        return reverse("issue:incident_detail", args={self.id})

    def __str__(self):
        return f"{self.type.name} - {self.employee.name}"


class Remark(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.RESTRICT, related_name="remarks")
    action = models.CharField(max_length=20, choices=Issue.STATUS)
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="remarks"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.issue} - {self.action}"
