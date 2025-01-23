from django.contrib import admin
from .models import (
    Customer,
    ColorStandard,
    Color,
    RawMaterial,
    Shift,
)

admin.site.register(Customer)
admin.site.register(ColorStandard)
admin.site.register(Color)
admin.site.register(RawMaterial)
admin.site.register(Shift)
