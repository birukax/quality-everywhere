from django.urls import path
from . import views

app_name = "report"

urlpatterns = [
    path(
        "assessment/get/<int:id>/",
        views.get_assessment_report,
        name="get_assessment_report",
    ),
    path("header/list", views.header_list, name="header_list"),
    path("header/create", views.create_header, name="create_header"),
    path("header/edit/<int:id>", views.edit_header, name="edit_header"),
]
