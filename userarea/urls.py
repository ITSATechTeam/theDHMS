from django.urls import path
from . import views


urlpatterns = [
    path('nav/', views.NavBar, name="NavBar"),
    # path('nav/', views.NavBar, name="NavBar"),
    path('dashboard/', views.Dashboard, name="Dashboard"),
    # path('uploaddevices/', views.UploadDevices, name="UploadDevices"),
    path('devicesinventory/', views.DeviceInventory, name="DeviceInventory"),
    path('staffmembers/', views.StaffMembers, name="StaffMembers"),
    path('reports/', views.Reports, name="Reports"),
    path('support/', views.Support, name="Support"),
    path('searchresult/', views.Searchresult, name="Searchresult"),
    path('maintainance/', views.Maintainance, name="Maintainance"),
    path('settings/', views.Settings, name="Settings"),
    path('staffdetails/<str:id>/', views.StaffDetails, name="StaffDetails"),
    path('registerStaff/<str:name>/', views.registerStaff, name="registerStaff"),
    path('editDeviceData/<str:deviceip>/', views.EditDeviceData, name="EditDeviceData"),
    path('editstaffdetails/<str:staffid>/', views.EditStaff, name="EditStaff"),
    path('editdevice/<str:deviceid>/', views.EditDevice, name="EditDevice"),
    # path('editprofile/', views.EditProfile, name="EditProfile"),
    path('scannetwork/', views.ScanNetwork, name="ScanNetwork"),
    path('logout/', views.Logout, name='Logout'),
    path('download_Sample_file/', views.downloadSampleFile, name="downloadSampleFile"),
    path('downloadsamplecsvheaders/', views.downloadSampleCSVHeaders, name="downloadSampleCSVHeaders"),
    # path('searchresult/', views.Searchresult, name='Searchresult'),
    path('downloadsamplecsv/', views.downloadSampleCSV, name="downloadSampleCSV"),
    path('deletedevice/<str:pk>/', views.DeleteDevice, name='DeleteDevice'),
    path('deletestaff/<str:pk>/', views.DeleteStaff, name='DeleteStaff'),
    path('editcompanydetails/<str:id>/', views.EditUserSignupDetails, name="EditUserSignupDetails"),
    path('profilepage/<str:pk>/', views.ProfilePage, name="ProfilePage"),
    path('uploadprofileimagepage/<str:pk>/', views.UploadProfileImg, name="UploadProfileImg"),
    path('testpage/', views.TestPage, name="TestPage"),
]
    

