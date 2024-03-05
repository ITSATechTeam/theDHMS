from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.All_Organization, name="All_Organization"),
    path('userlogout/<str:pk>/', views.User_Logout, name="User_Logout"),
    path('orgprofile/<str:pk>/', views.Org_Profile, name="Org_Profile"),
    path('orgdevices/<str:UniqueID>/', views.View_Org_All_Devices, name="View_Org_All_Devices"),
    path('orglogin/', views.User_Login, name="User_Login"),
    path('regorg/', views.Register_Org, name="Register_Org"),
    path('alldevices/', views.View_All_Devices, name="View_All_Devices"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



