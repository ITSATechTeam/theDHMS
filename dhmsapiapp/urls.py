from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.All_Organization, name="All_Organization"),
    path('userlogout/', views.User_Logout, name="User_Logout"),
    path('orgprofile/', views.Org_Profile, name="Org_Profile"),
    # path('orgprofile/<str:pk>/', views.Org_Profile, name="Org_Profile"),
    path('orgdevices/<str:UniqueID>/', views.View_Org_All_Devices, name="View_Org_All_Devices"),
    path('orgstaff/<str:UniqueID>/', views.View_Org_Staff, name="View_Org_Staff"),
    path('orglogin/', views.User_Login, name="User_Login"),
    path('regorg/', views.Register_Org, name="Register_Org"),
    path('regstaff/', views.Register_Staff, name="Register_Staff"),
    path('alldevices/', views.View_All_Devices, name="View_All_Devices"),
    path('allstaff/', views.View_All_Staff, name="View_All_Staff"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



