from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
