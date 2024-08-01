from django.urls import path
from . import views


urlpatterns = [
    path('', views.DefaultView, name="DefaultView"),
    path('studentLogin/', views.StudentLogin, name="StudentLogin"),
    path('studentdashboard/', views.StudentDashboard, name="StudentDashboard"),
]


