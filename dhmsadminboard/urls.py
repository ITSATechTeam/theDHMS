from django.urls import path
from . import views


urlpatterns = [
    path('', views.SuperAdminDashboard, name="SuperAdminDashboard"),
    path('adminlogin/', views.SuperAdminAccess, name="SuperAdminAccess"),
    path('adminsignup/', views.SuperAdminAccessSignup, name="SuperAdminAccessSignup"),
    path('adminnav/', views.AdminNavBar, name="AdminNavBar"),
    path('switcher/', views.SuperAdminSwitcher, name="SuperAdminSwitcher"),
    path('devices/', views.AllDevices, name="AllDevices"),
    path('adminmaintenance/', views.AdminMaintenance, name="AdminMaintenance"),
    path('partners/', views.ITPartners, name="ITPartners"),
    path('adminreports/', views.SuperAdminReports, name="SuperAdminReports"),
    path('adminsettings/', views.SuperAdminSettings, name="SuperAdminSettings"),
    path('organizations/', views.Organizations, name="Organizations"),
    path('adminlogout/', views.AdminLogout, name="AdminLogout"),
    path('organizations/<str:pk>/', views.OrganizationsDetails, name="OrganizationsDetails"),
]


