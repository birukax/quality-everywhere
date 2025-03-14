from django.urls import path
from . import views

app_name = "approval"

urlpatterns = [
    path("assessments/<str:type>", views.assessment_list, name="assessment_list"),
    path(
        "assessment/create/<int:id>",
        views.create_assessment_approval,
        name="create_assessment_approval",
    ),
    path(
        "assessment/approve/<int:id>",
        views.approve_assessment,
        name="approve_assessment",
    ),
    path(
        "assessment/reject/<int:id>", views.reject_assessment, name="reject_assessment"
    ),
    path("fire-preventions", views.fire_prevention_list, name="fire_prevention_list"),
    path(
        "fire-prevention/create/<int:id>",
        views.create_fire_prevention_approval,
        name="create_fire_prevention_approval",
    ),
    path(
        "fire-prevention/approve/<int:id>",
        views.approve_fire_prevention,
        name="approve_fire_prevention",
    ),
    path(
        "fire-prevention/reject/<int:id>",
        views.reject_fire_prevention,
        name="reject_fire_prevention",
    ),
]
