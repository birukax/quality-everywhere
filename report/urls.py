from django.urls import path
from . import views

app_name = "report"

urlpatterns = [
    path("get/<int:id>/", views.get_report, name="get_report"),
]
