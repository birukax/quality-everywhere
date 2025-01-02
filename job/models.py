from django.db import models
from django.urls import reverse
from .validators import validate_artwork


class Job(models.Model):
    no = models.CharField(max_length=100)
    tests = models.IntegerField(default=1)
    product = models.ForeignKey("misc.Product", on_delete=models.CASCADE)
    customer = models.ForeignKey(
        "misc.Customer", on_delete=models.CASCADE, null=True, blank=True
    )
    machine = models.ForeignKey(
        "misc.Machine", on_delete=models.CASCADE, null=True, blank=True
    )
    color_standard = models.ForeignKey(
        "misc.ColorStandard", on_delete=models.CASCADE, null=True, blank=True
    )
    certificate_no = models.CharField(max_length=100, null=True, blank=True)
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
