from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.StartApp, name="StartApp"),
    path('', views.save_applications, name='save_applications'),
    path('savedevicehealth', views.saveDeviceHealthInfo, name='saveDeviceHealthInfo'),
    ]


