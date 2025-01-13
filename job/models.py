from django.db import models
from django.urls import reverse
from .validators import validate_artwork

STATUS = (
    ("CREATED", "CREATED"),
    ("FIRST-OFF CREATED", "FIRST-OFF CREATED"),
    ("FIRST-OFF PENDING", "FIRST-OFF PENDING"),
    ("FIRST-OFF COMPLETED", "FIRST-OFF COMPLETED"),
    ("ON-PROCESS", "ON-PROCESS"),
    # ("ON-PROCESS PENDING", "ON-PROCESS PENDING"),
    # ("ON-PROCESS COMPLETED", "ON-PROCESS COMPLETED"),
    ("COMPLETED", "COMPLETED"),
)


class Job(models.Model):
    no = models.CharField(max_length=100)
    tests = models.IntegerField(default=1)
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
    current_machine = models.ForeignKey(
        "machine.Machine",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="current_jobs",
    )
    color_standard = models.ForeignKey(
        "misc.ColorStandard", on_delete=models.CASCADE, null=True, blank=True
    )
    certificate_no = models.CharField(max_length=100, null=True, blank=True)
    artwork_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=STATUS, default="CREATED")
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
