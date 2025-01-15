from django.contrib import admin
from .models import FirstOff, OnProcess, Test, Conformity, Assessment

admin.site.register(Assessment)
admin.site.register(FirstOff)
admin.site.register(OnProcess)
admin.site.register(Test)
admin.site.register(Conformity)
