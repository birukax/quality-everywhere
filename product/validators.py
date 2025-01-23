from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.template.defaultfilters import filesizeformat


def validate_artwork(file):
    max_size = 10 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError(
            f"Please keep filesize under {filesizeformat(max_size)}. Current filesize {filesizeformat(file.size)}"
        )

    try:
        image = get_image_dimensions(file)
        if not image:
            raise ValidationError("Invalid image file")
    except Exception:
        raise ValidationError("Invalid image file")
