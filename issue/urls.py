from django.urls import path
from . import views

app_name = "issue"

urlpatterns = [
    path("list", views.list, name="list"),
    path("create", views.create, name="create"),
    # path("edit/<int:id>", views.edit, name="edit"),
    path("detail/<int:id>", views.detail, name="detail"),
    path("location/list", views.location_list, name="location_list"),
    path("location/create", views.create_location, name="create_location"),
    path("type/list", views.issue_type_list, name="issue_type_list"),
    path("type/create", views.create_issue_type, name="create_issue_type"),
]
