from django.urls import path
from . import views


urlpatterns = [
    path('', views.SuperAdminAccess, name="SuperAdminAccess"),
]


