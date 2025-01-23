from django.urls import reverse
from django.db import models
from .validators import validate_artwork


class Product(models.Model):
    no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]

    def get_absolute_url(self):
        return reverse("product:detail", args={self.id})


class Artwork(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="artworks"
    )
    file = models.FileField(
        upload_to="artworks/",
        validators=[validate_artwork],
        help_text="Upload artwork file",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    class Meta:
        ordering = ["-id"]
