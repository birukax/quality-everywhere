from django.urls import path
from .import views

app_name = 'approval'

urlpatterns = [
    path('first_offs/', views.first_offs, name='first_offs'),
    path('first_off/create/<int:id>/', views.create_first_off_approval, name='create_first_off_approval'),
]