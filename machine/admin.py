from django.contrib import admin
from .models import Machine, Route, MachineRoute


admin.site.register(Machine)
admin.site.register(Route)
admin.site.register(MachineRoute)
