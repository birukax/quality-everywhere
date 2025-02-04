from django.contrib import admin
from .models import (
    FirstOff,
    OnProcess,
    Test,
    Conformity,
    Assessment,
    Waste,
    SemiWaste,
    Viscosity,
    Lamination,
    Substrate,
)

admin.site.register(Assessment)
admin.site.register(FirstOff)
admin.site.register(OnProcess)
admin.site.register(Test)
admin.site.register(Conformity)
admin.site.register(Waste)
admin.site.register(Viscosity)
admin.site.register(SemiWaste)
admin.site.register(Lamination)
admin.site.register(Substrate)
