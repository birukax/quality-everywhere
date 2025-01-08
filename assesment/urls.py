from django.urls import path
from . import views

app_name = "assesment"

urlpatterns = [
    path("test/list", views.test_list, name="test_list"),
    path("test/create", views.create_test, name="create_test"),
    path("test/<int:id>/edit", views.edit_test, name="edit_test"),
    path("conformity/list", views.conformity_list, name="conformity_list"),
    path("conformity/create", views.create_conformity, name="create_conformity"),
    path("conformity/<int:id>/edit", views.edit_conformity, name="edit_conformity"),
]
