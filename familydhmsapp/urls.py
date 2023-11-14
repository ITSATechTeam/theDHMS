from django.urls import path
from . import views


urlpatterns = [
    path('register', views.UserReg, name="UserReg"),
    path('login', views.UserLogin, name="UserLogin"),
    path('', views.FamilyDHMSDashboard, name="FamilyDHMSDashboard"),
    path('familyinventory', views.FamilyInventory, name="FamilyInventory"),
    path('familysupport', views.FamilySupport, name="FamilySupport"),
    path('familymaintain', views.FamilyMaintenance, name="FamilyMaintenance"),
    path('familyanalytics', views.FamilyAnalytics, name="FamilyAnalytics"),
    path('familymember', views.FamilyMembers, name="FamilyMembers"),
    path('familysettings', views.FamilySettings, name="FamilySettings"),
    path('familylogout', views.FamilyLogout, name="FamilyLogout"),
    # path('logout', views.UserLogout, name="UserLogout"),
    # path('maintenancedetails/<str:name>/', views.MaintainanceDetails, name="MaintainanceDetails"),
]


