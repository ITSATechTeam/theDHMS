from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomTokenObtainPair
# from .views import custom_token_refresh

# JWT IMPORTS
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # path('', views.All_Organization, name="All_Organization"),
    path('userlogout', views.User_Logout, name="User_Logout"),
    path('orgprofile', views.Org_Profile, name="Org_Profile"),
    # path('orgprofile/<str:pk>/', views.Org_Profile, name="Org_Profile"),
    path('orgdevices/<str:UniqueID>', views.View_Org_All_Devices, name="View_Org_All_Devices"),
    path('orgstaff/<str:UniqueID>', views.View_Org_Staff, name="View_Org_Staff"),
    path('orglogin', views.User_Login, name="User_Login"),
    path('regorg', views.Register_Org, name="Register_Org"),
    path('regstaff', views.Register_Staff, name="Register_Staff"),
    path('alldevices', views.View_All_Devices, name="View_All_Devices"),
    path('allstaff', views.View_All_Staff, name="View_All_Staff"),
    # STUDENT DHMS ENDPOINTS STARTS HERE
    path('studentreg', views.Student_Registration, name="Student_Registration"),
    path('studentdevreg', views.Student_Device_Registration, name="Student_Device_Registration"),
    path('substudentreg', views.Sub_Student_Registration, name="Sub_Student_Registration"),
    path('studentlogin', views.Student_Login, name="Student_Login"),
    path('changepassword', views.RequestPasswordUpdate, name="RequestPasswordUpdate"),
    # TECHNICAL PARTNERS ENDPOINTS STARTS HERE
    path('findtechnicalpartner', views.Find_Technical_Partner, name="Find_Technical_Partner"),
    path('technicalpartners', views.Technical_Partners, name="Technical_Partners"),
    # ITSA SUPER ADMIN ENDPOINT
    path('superadminlogin', views.ItsaSuperAdminLoginFxn, name="ItsaSuperAdminLoginFxn"),
    # GET MAINTENANCE REQS PER MONTH ENDPOINT
    path('getmaintenancereqs', views.MaintenanceReqPerMonth, name="MaintenanceReqPerMonth"),
    # GET LOGGED IN STUDENT DEVICES
    path('getstudentdevices', views.GetAllStudentDevices, name="GetAllStudentDevices"),
    path('getsinglestudentdevices/<str:id>', views.GetSingleStudentDevices, name="GetSingleStudentDevices"),
    # GET ALL REGISTERED STUDENTS
    path('getstudents', views.GetAllRegStudents, name="GetAllRegStudents"),
    path('getstudents/<str:id>', views.GetSingleStudents, name="GetAllRegStudents"),
    # EDIT A REGISTERED STUDENTS
    path('editstudentdata/<str:id>', views.EditStudentData, name="EditStudentData"),
    # EDIT A REGISTERED DEVICE
    path('editdevicedata/<str:id>', views.EditDeviceData, name="EditDeviceData"),
    # DELETE A REGISTERED DEVICE
    path('deletedevicedata/<str:id>', views.DeleteDeviceData, name="DeleteDeviceData"),
    # DELETE A REGISTERED STUDENT
    path('deletestudentdata/<str:id>', views.DeleteStudentData, name="DeleteStudentData"),
    # JWT TOKEN ENDPOINTS
    path('generatetoken', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken', TokenRefreshView.as_view(), name='token_refresh'),
    # 
    # path('refreshtoken', CustomTokenObtainPair, name='TokenObtainPefresh'),
    # path('api/token/refresh/', custom_token_refresh, name='token_refresh'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



