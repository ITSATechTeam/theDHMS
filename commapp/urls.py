from django.urls import path
from . import views


urlpatterns = [
    path('', views.CommDashboard, name="CommDashboard"),
    path('startaudiocall/', views.StartAudioCall, name="StartAudioCall"),
]


