from django.contrib import admin
from .models import (
    IssueType,
    Issue,
    Location,
    Remark,
    Department,
    Employee,
    Incident,
    IncidentType,
    FirePrevention,
    FPChecklist,
    Checkpoint,
)

admin.site.register(Issue)
admin.site.register(IssueType)
admin.site.register(Location)
admin.site.register(Remark)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(IncidentType)
admin.site.register(Incident)
admin.site.register(FirePrevention)
admin.site.register(FPChecklist)
admin.site.register(Checkpoint)
