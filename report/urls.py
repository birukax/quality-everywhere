from django.urls import path
from . import views

app_name = "report"

urlpatterns = [
    path("test", views.test, name="test"),
]
