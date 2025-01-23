from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("list", views.list, name="list"),
    path("detail/<int:id>", views.detail, name="detail"),
    path("artwork/list", views.artwork_list, name="artwork_list"),
    path("artwork/detail/<int:id>", views.artwork_detail, name="artwork_detail"),
    path("artwork/add/<int:id>", views.add_artwork, name="add_artwork"),
    path("artwork/edit/<int:id>", views.edit_artwork, name="edit_artwork"),
    path("get", views.get, name="get"),
]
