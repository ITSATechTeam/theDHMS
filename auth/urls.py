from django.urls import path
from . import views


urlpatterns = [
    path('redirect/', views.AuthRedirect, name="AuthRedirect"),
]

