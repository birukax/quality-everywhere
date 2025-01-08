from django.contrib import admin
from .models import (
    Customer,
    ColorStandard,
    Color,
    Product,
    Paper,
    Shift,
)

admin.site.register(Customer)
admin.site.register(ColorStandard)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(Paper)
admin.site.register(Shift)
