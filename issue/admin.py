from django.contrib import admin
from .models import IssueType, Issue, Location, Remark

admin.site.register(Issue)
admin.site.register(IssueType)
admin.site.register(Location)
admin.site.register(Remark)
