from django.urls import path
from . import views


urlpatterns = [
    path('staffnav/', views.StaffNavBar, name="StaffNavBar"),
    path('staffdashboard/', views.StaffDashboard, name="StaffDashboard"),
    path('stafflogin/', views.StaffLogin, name="StaffLogin"),
    path('stafflogout/', views.StaffLogout, name='StaffLogout'),
    path('staffsolution/', views.StaffSolution, name='StaffSolution'),
    path('staffsettings/', views.StaffSetting, name='StaffSetting'),
    path('staffDeviceInventory/', views.StaffDeviceInventory, name='StaffDeviceInventory'),
    path('staffviewdevicedetails/<str:name>/', views.StaffViewDeviceDetails, name="StaffViewDeviceDetails"),
    path('staffsearchresult/', views.StaffSearchresult, name="StaffSearchresult"),
    path('staffmaintenancerequests/', views.StaffMaintainance, name="StaffMaintainance"),
    path('staffmaintenancdetail/<str:name>/', views.StaffMaintainanceDetails, name="StaffMaintainanceDetails"),
    path('staffeditmaintenancdetail/<str:name>/', views.EditStaffMaintainanceDetails, name="EditStaffMaintainanceDetails"),
    # path('staffdetails/<str:id>/', views.StaffDetails, name="StaffDetails"),
    path('staffdeletecomment/<str:pk>/<str:name>/', views.StaffDeleteAddedComment, name="StaffDeleteAddedComment"),
    path('azuresignin/', views.AzureSignin, name="AzureSignin"),
    path('redirect/', views.AuthRedirect, name="AuthRedirect"),
    path('index/', views.index, name="index"),
    path('secret/', views.secret_page, name="secret"),
    path('organizations/', views.organizations, name="organizations"),
]

