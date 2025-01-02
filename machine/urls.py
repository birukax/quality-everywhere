from django.urls import path
from . import views

app_name = "machine"

urlpatterns = [
    path("list", views.list, name="list"),
    path("create", views.create, name="create"),
    path("<int:id>/edit", views.edit, name="edit"),
]
