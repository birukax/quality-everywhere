import os
from django.urls import reverse
from django.db import models
from django.db.models.functions import Lower
from main.validators import validate_image, validate_code
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, Thumbnail


def artwork_upload_path(instance, filename):
    ext = filename.split(".")[-1]

    new_filename = f"{instance.product.name}-{instance.code}.{ext}"

    return os.path.join("artworks/", new_filename)


class Product(models.Model):
    no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-no", "name"]

    def get_absolute_url(self):
        return reverse("product:detail", args={self.id})


class Artwork(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="artworks"
    )
    code = models.CharField(
        max_length=20,
        validators=[validate_code],
    )
    approved = models.BooleanField(default=False)
    remark = models.TextField(null=True, blank=True)
    file = models.FileField(
        upload_to=artwork_upload_path,
        validators=[validate_image],
        help_text="Upload artwork file",
    )
    file_thumbnail = ImageSpecField(
        source="file",
        processors=[Thumbnail(128, crop=False)],
        format="PNG",
        options={"quality": 100},
    )
    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="created_artworks",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.product.name})"

    class Meta:

        constraints = [
            models.UniqueConstraint(
                Lower("code"), name="unique_case_insensitive_artwork_code"
            )
        ]
        ordering = ["-id"]
