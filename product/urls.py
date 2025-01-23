from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("list", views.list, name="list"),
    path("get", views.get, name="get"),
]
