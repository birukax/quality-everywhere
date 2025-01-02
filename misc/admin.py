from django.contrib import admin
from .models import (
    Customer,
    ColorStandard,
    Color,
    Product,
    Paper,
    Shift,
    Test,
    Unit,
)

admin.site.register(Customer)
admin.site.register(ColorStandard)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(Paper)
admin.site.register(Shift)
admin.site.register(Test)
admin.site.register(Unit)
