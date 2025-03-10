from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from PIL import Image
import os


def validate_ratio_format(value):
    parts = value.split(":")
    if len(parts) != 2:
        raise ValidationError(_('Invalid ratio format. Use "X:Y" (e.g., 100:25).'))

    try:
        x, y = int(parts[0]), int(parts[1])
    except ValueError:
        raise ValidationError(_("Both values must be integers."))
    if x > 100 or y > 100:
        raise ValidationError(_("Values cannot exceed 100."))


def validate_image(file):
    max_size = 10 * 1024 * 1024
    valid_extensions = [".jpg", ".jpeg", ".png", ".webp", ".tiff", ".bmp"]
    ext = os.path.splitext(file.name)[1].lower()

    if file.size > max_size:
        raise ValidationError(
            _(
                f"Please keep filesize under {filesizeformat(max_size)}. Current filesize {filesizeformat(file.size)}"
            )
        )
    if ext not in valid_extensions:
        raise ValidationError(
            _(f"Unsupported file extension. Only image files are allowed.")
        )
    try:
        with Image.open(file) as img:
            img.verify()
    except Exception:
        raise ValidationError(_("Invalid image file."))


def validate_artwork(file):
    pass


def validate_code(value):
    if " " in value:
        raise ValidationError(_("Code should not contain spaces"))
