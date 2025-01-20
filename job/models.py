from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .validators import validate_artwork

STATUS = (
    ("READY", "READY"),
    ("FIRST-OFF CREATED", "FIRST-OFF CREATED"),
    # ("FIRST-OFF PENDING", "FIRST-OFF PENDING"),
    ("FIRST-OFF COMPLETED", "FIRST-OFF COMPLETED"),
    ("ON-PROCESS CREATED", "ON-PROCESS CREATED"),
    # ("ON-PROCESS PENDING", "ON-PROCESS PENDING"),
    ("ON-PROCESS COMPLETED", "ON-PROCESS COMPLETED"),
    ("COMPLETED", "COMPLETED"),
)


class Job(models.Model):
    no = models.CharField(max_length=100)
    product = models.ForeignKey("misc.Product", on_delete=models.CASCADE)
    customer = models.ForeignKey(
        "misc.Customer", on_delete=models.CASCADE, null=True, blank=True
    )
    press_machine = models.ForeignKey(
        "machine.Machine",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="jobs",
    )
    route = models.ForeignKey(
        "machine.Route", on_delete=models.CASCADE, null=True, blank=True
    )
    color_standard = models.ForeignKey(
        "misc.ColorStandard", on_delete=models.CASCADE, null=True, blank=True
    )
    certificate_no = models.CharField(max_length=100, null=True, blank=True)
    artwork_approved = models.BooleanField(default=False)
    artwork = models.FileField(
        upload_to="artworks/",
        null=True,
        blank=True,
        validators=[validate_artwork],
        help_text="Upload artwork file",
    )

    class Meta:
        ordering = ["-no"]

    def __str__(self):
        return f"{self.no } - {self.product.name}"

    def get_absolute_url(self):
        return reverse("job:detail", args={self.id})


class JobTest(models.Model):

    status = models.CharField(max_length=100, choices=STATUS, default="READY")
    job = models.ForeignKey(
        "job.Job", on_delete=models.CASCADE, related_name="job_tests"
    )

    current_machine = models.ForeignKey(
        "machine.Machine",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="current_job_tests",
    )
    paper = models.ForeignKey("misc.Paper", on_delete=models.CASCADE)
    route = models.ForeignKey(
        "machine.Route", on_delete=models.CASCADE, null=True, blank=True
    )
    color_standard = models.ForeignKey(
        "misc.ColorStandard", on_delete=models.CASCADE, null=True, blank=True
    )
    batch_no = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_job_tests",
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.job.no } - {self.job.product.name} | {self.id}"

    def get_absolute_url(self):
        return reverse("job:test_detail", args={self.id})
