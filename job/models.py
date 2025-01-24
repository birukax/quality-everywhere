from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="jobs"
    )
    customer = models.ForeignKey(
        "misc.Customer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="jobs",
    )
    route = models.ForeignKey(
        "machine.Route",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="jobs",
    )
    color_standard = models.ForeignKey(
        "misc.ColorStandard",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="jobs",
    )
    # certificate_no = models.CharField(max_length=100, null=True, blank=True)

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
    artwork = models.ForeignKey(
        "product.Artwork", on_delete=models.RESTRICT, related_name="job_tests"
    )
    current_machine = models.ForeignKey(
        "machine.Machine",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="current_job_tests",
    )
    raw_material = models.ForeignKey("misc.RawMaterial", on_delete=models.CASCADE)
    route = models.ForeignKey(
        "machine.Route",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="job_tests",
    )
    color_standard = models.ForeignKey(
        "misc.ColorStandard",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="job_tests",
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
