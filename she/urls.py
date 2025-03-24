from django.urls import path
from . import views

app_name = "she"

urlpatterns = [
    # path("edit/<int:id>", views.edit, name="edit"),
    path("issue/list", views.issue_list, name="issue_list"),
    path("issue/create", views.create_issue, name="create_issue"),
    path("issue/detail/<int:id>", views.issue_detail, name="issue_detail"),
    path(
        "status/update/<int:id>/<str:action>", views.update_status, name="update_status"
    ),
    path("incident/list", views.incident_list, name="incident_list"),
    path("incident/create", views.create_incident, name="create_incident"),
    path("incident/detail/<int:id>", views.incident_detail, name="incident_detail"),
    path("department/list", views.department_list, name="department_list"),
    path("department/get", views.get_departments, name="get_departments"),
    path("employee/list", views.employee_list, name="employee_list"),
    path("employee/get", views.get_employees, name="get_employees"),
    path("location/list", views.location_list, name="location_list"),
    path("location/create", views.create_location, name="create_location"),
    path("location/edit/<int:id>", views.edit_location, name="edit_location"),
    path("issue/type/list", views.issue_type_list, name="issue_type_list"),
    path("issue/type/create", views.create_issue_type, name="create_issue_type"),
    path("issue/type/edit/<int:id>", views.edit_issue_type, name="edit_issue_type"),
    path("incident/type/list", views.incident_type_list, name="incident_type_list"),
    path(
        "incident/type/create", views.create_incident_type, name="create_incident_type"
    ),
    path(
        "incident/type/edit/<int:id>",
        views.edit_incident_type,
        name="edit_incident_type",
    ),
    path(
        "fire-prevention/list", views.fire_prevention_list, name="fire_prevention_list"
    ),
    path(
        "fire-prevention/create",
        views.create_fire_prevention,
        name="create_fire_prevention",
    ),
    path(
        "fire-prevention/detail/<int:id>",
        views.fire_prevention_detail,
        name="fire_prevention_detail",
    ),
    path(
        "fire-prevention/checklist/save/<int:id>",
        views.save_fp_checklist,
        name="save_fp_checklist",
    ),
    path(
        "fire-prevention/checkpoint/list", views.checkpoint_list, name="checkpoint_list"
    ),
    path(
        "fire-prevention/checkpoint/create",
        views.create_checkpoint,
        name="create_checkpoint",
    ),
    path(
        "fire-prevention/checkpoint/edit/<int:id>",
        views.edit_checkpoint,
        name="edit_checkpoint",
    ),
]
