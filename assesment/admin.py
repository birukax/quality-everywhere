from django.contrib import admin
from .models import FirstOffTest, OnProcessConformity, Test, Conformity

admin.site.register(FirstOffTest)
admin.site.register(OnProcessConformity)
admin.site.register(Test)
admin.site.register(Conformity)
