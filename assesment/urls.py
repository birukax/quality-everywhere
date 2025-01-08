from django.urls import path
from . import views

app_name = "assesment"

urlpatterns = [
    path("test/list", views.test_list, name="test_list"),
    path("test/create", views.create_test, name="create_test"),
    path("test/<int:id>/edit", views.edit_test, name="edit_test"),
]
