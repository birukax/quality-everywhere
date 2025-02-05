from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)


class IssueType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)


class Issue(models.Model):
    STATUS = (
        ("CREATED", "CREATED"),
        ("PENDING", "PENDING"),
        ("REJECTED", "REJECTED"),
        ("COMPLETED", "COMPLETED"),
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
    description = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="issues"
    )

    def __str__(self):
        return f"{self.issue_type} - {self.location}"


class Remark(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.RESTRICT, related_name="remarks")
    action = models.CharField(max_length=20, choices=Issue.STATUS)
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name="remarks"
    )
