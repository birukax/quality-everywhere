from django.urls import path
from . import views

app_name = "report"

urlpatterns = [
    path(
        "assessment/get/<int:id>",
        views.get_assessment_report,
        name="get_assessment_report",
    ),
    path(
        "assessments/get/<int:id>",
        views.get_assessments_report,
        name="get_assessments_report",
    ),
    path(
        "fire-prevention/get/<int:id>",
        views.get_fire_prevention_report,
        name="get_fire_prevention_report",
    ),
    path(
        "incident/get/<int:id>",
        views.get_incident_report,
        name="get_incident_report",
    ),
    path("header/list", views.header_list, name="header_list"),
    path("header/create", views.create_header, name="create_header"),
    path("header/edit/<int:id>", views.edit_header, name="edit_header"),
]
