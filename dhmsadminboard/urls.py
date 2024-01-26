from django.urls import path
from . import views


urlpatterns = [
    path('', views.SuperAdminAccess, name="SuperAdminAccess"),
    path('switcher/', views.SuperAdminSwitcher, name="SuperAdminSwitcher"),
]


