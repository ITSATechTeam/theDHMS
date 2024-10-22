from django.urls import path
from . import views
from . import viewsadminapi
from .views import *
from . import technicalappviews
from django.conf import settings
from django.conf.urls.static import static
# from .views import custom_token_refresh

# JWT IMPORTS
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # WEBHOOK URL
    # path('webhook/', WebhookView.as_view(), name='webhook'),
    path('paystackwebhook', PaystackWebhookView, name='PaystackWebhookView'),
    path('allorgs', viewsadminapi.FetchAllOrganization, name="FetchAllOrganization"),
    path('organizationdetails', viewsadminapi.FetchOrganizationDetails, name="FetchOrganizationDetails"),
    # path('userlogout', views.User_Logout, name="User_Logout"),
    # path('orgprofile', views.Org_Profile, name="Org_Profile"),
    # # path('orgprofile/<str:pk>/', views.Org_Profile, name="Org_Profile"),
    # path('orgdevices/<str:UniqueID>', views.View_Org_All_Devices, name="View_Org_All_Devices"),
    # path('orgstaff/<str:UniqueID>', views.View_Org_Staff, name="View_Org_Staff"),
    # path('orglogin', views.User_Login, name="User_Login"),
    # path('regorg', views.Register_Org, name="Register_Org"),
    # path('regstaff', views.Register_Staff, name="Register_Staff"),
    # path('alldevices', views.View_All_Devices, name="View_All_Devices"),
    # path('allstaff', views.View_All_Staff, name="View_All_Staff"),
    # FETCH ALL GENERAL SUPER USER MAINTENANCE REQUEST 
    path('getallmaintenancereqs', viewsadminapi.GetAllDHMSMaintenanceReqs, name="GetAllDHMSMaintenanceReqs"),
    # GET DEVICE CONDITION STATUS ENUM
    path('devicestatus', views.Device_Health_Status, name="Device_Health_Status"),
    # STUDENT DHMS ENDPOINTS STARTS HERE
    path('studentreg', views.Student_Registration, name="Student_Registration"),
    path('studentdevicereg', views.Student_Device_Registration, name="Student_Device_Registration"),
    path('substudentreg', views.Sub_Student_Registration, name="Sub_Student_Registration"),
    path('studentlogin', views.Student_Login, name="Student_Login"),
    # PASSWORD CHANGE ENDPOINTS
    path('changepassword', views.RequestPasswordUpdate, name="RequestPasswordUpdate"),
    path('addnewpassword', views.AddNewPassword, name="AddNewPassword"),
    
    # TECHNICAL PARTNERS ENDPOINTS STARTS HERE
    # REGISTER A TECHNICAL PARTNER
    path('registertechnician', technicalappviews.RegisterTechnicalPartner, name="RegisterTechnicalPartner"),
    # LOGIN A TECHNICAL PARTNER
    path('technicianlogin', technicalappviews.TechnicianPartnerLogin, name="TechnicianPartnerLogin"),
    # FIND A SINGLE TECHNICAL PARTNER
    path('findtechnicalpartner', views.GetTechnicalPartnerProfile, name="GetTechnicalPartnerProfile"),
    # FETCH ALL TECHNICAL PARTNERS
    path('technicalpartners', views.Technical_Partners, name="Technical_Partners"),
    # FETCH TECHNICAL PARTNERS
    path('fetchtechnicians', views.FetchTechnicalPartners, name='FetchTechnicalPartners'),    
    # FETCH MAINTENANCE REQUEST COUNT
    path('getmaintenancerequestscount', technicalappviews.GetAllMaintenanceCount, name='GetAllMaintenanceCount'),    
    # FETCH ALL MAINTENANCE REQUEST
    path('getallmaintenancerequests', technicalappviews.GetAllMaintenanceRequest, name='GetAllMaintenanceRequest'),    
    # FETCH MAINTENANCE COMPLETION PERCENTAGE
    path('getcompletemaintenancepercentrate', technicalappviews.GetCompletedMaintenancePercentage, name='GetCompletedMaintenancePercentage'),    
    # FETCH PENDING MAINTENANCE REQUEST
    path('getpendingmaintenancereqs', technicalappviews.GetPendingMaintenanceRequest, name='GetPendingMaintenanceRequest'),    
    # FETCH COMPLETED MAINTENANCE REQUEST
    path('getcompletedmaintenancereqs', technicalappviews.GetCompletedMaintenanceRequest, name='GetCompletedMaintenanceRequest'),    
    # FETCH ONGOING MAINTENANCE REQUEST
    path('getongoingmaintenancereqs', technicalappviews.GetOngoingMaintenanceRequest, name='GetOngoingMaintenanceRequest'),    
    # FETCH DECLINED MAINTENANCE REQUEST
    path('getdeclineddmaintenancereqs', technicalappviews.GetDeclinedMaintenanceRequest, name='GetDeclinedMaintenanceRequest'),    
    # FETCH MAINTENANCE REQEUSTS PER MONTH
    path('fetchmaintenancepermonth', technicalappviews.FetchMaintenanceRequestPerMonth, name='FetchMaintenanceRequestPerMonth'),    
    # FETCH MAINTENANCE TYPE RATE
    path('getmaintenancetyperate', technicalappviews.GetMaintenanceTypePercentage, name='GetMaintenanceTypePercentage'),    
    # FETCH LASTEST FIVEMAINTENANCE REQEUSTS
    path('getlastfivemaintenacereqs', technicalappviews.GetLatestFiveMaintenanceRequest, name='GetLatestFiveMaintenanceRequest'),    
    # TECHNICAL PARTNERS ENDPOINTS STARTS HERE
     
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
    # EDIT ADMIN STUDENT
    path('editadminstudent', views.EditAdminStudentData, name="EditAdminStudentData"),
    # DELETE A REGISTERED DEVICE
    path('deletedevicedata/<str:id>', views.DeleteDeviceData, name="DeleteDeviceData"),
    # DELETE A REGISTERED STUDENT
    path('deletestudentdata/<str:id>', views.DeleteStudentData, name="DeleteStudentData"),
    # JWT TOKEN ENDPOINTS
    path('generatetoken', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken', TokenRefreshView.as_view(), name='token_refresh'),
    # UNASSIGN DEVICE FROM ANY STUDENT AND ASSIGN TO STUDENT ADMIN
    path('unassigndeviceuser/<str:id>', views.UnassignDevice, name="UnassignDevice"),
    # REQUEST FOR MAINTENANCE
    path('reqmaintenenace', views.MaintenanceReg, name="MaintenanceReg"),
    path('fetchmaintenance', views.FetchMaintenaceRequests, name="FetchMaintenaceRequests"),
    # REQUEST EMAIL VALIDATION CODE
    path('getemailcode', views.GetEmailValidationCode, name="GetEmailValidationCode"),
    path('validatecode', views.ValidateEmailCode, name="ValidateEmailCode"),
    # REQUEST PHONE NUMBER VALIDATION CODE
    path('getphonenumbercode', views.GetPhoneNumberValidationCode, name="GetPhoneNumberValidationCode"),
    path('validatephonenumbercode', views.ValidatePhoneCode, name="ValidatePhoneCode"),
    # path('verifyemail', views.VerifyEmailAddress, name="VerifyEmailAddress"),
    # REQUEST EMAIL VALIDATION CODE
    path('createpin', views.CreateTransactionPIN, name="CreateTransactionPIN"),
    path('updatetransactionpin', views.UpdateTransactionPIN, name="UpdateTransactionPIN"),
    # PAYSTACK RELATED ENDPOINTS
    path('registerpaystackcustomer', views.CreatePaystackCustomer, name="CreatePaystackCustomer"),
    path('findpaystackcustomerprofile', views.FindPaystackCustomer, name="FindPaystackCustomer"),
    path('creatededicatedwallet', views.CreateDedicatedVirtualAccount, name="CreateDedicatedVirtualAccount"),
    path('listbanks', views.PaystackListofBanks, name="PaystackListofBanks"),
    path('listalldva', views.List_DVAs, name="List_DVAs"),
    path('validatepaystackcustomer', views.ValidatePayStackCustomer, name="ValidatePayStackCustomer"),
    path('fetchwalletdetails', views.FetchWalletDetails, name="FetchWalletDetails"),
    path('findaccountname', views.VerifyUserAccountDetails, name="VerifyUserAccountDetails"),
    # path('createtransferrecipient', views.create_transfer_recipient, name="create_transfer_recipient"),
    # path('initializetransfer', views.initialize_transfer, name="initialize_transfer"),
    path('fetchalltransactions', views.FetchAllTransactions, name="FetchAllTransactions"),
    path('findaccountbalance', views.Calculate_balance, name="Calculate_balance"),
    path('fetch-transactions', views.fetch_and_save_transactions, name='fetch_transactions'),
    # CHECK KYC REQUIREMENT COMPLETION: EMAIL, PHONE, PIN CALIDATED.
    path('checkvalidationstatus', views.CheckKYCValidation, name='CheckKYCValidation'),
    # CHECK KYC REQUIREMENT COMPLETION: EMAIL, PHONE, PIN CALIDATED.
    path('transferfunds', views.StudentPlaceTransferRequest, name='StudentPlaceTransferRequest'),
    # FETCH OVERVIEW DETAILS
    path('dashboardoverview', views.DashboardOverview, name='DashboardOverview'),
    # CHECK STUDENT SUSCRIPTION PLAN
    path('checkstudentplan', views.CheckStudentPlan, name='CheckStudentPlan'),
    # FETCH MAINTENANCE COUNTS
    path('fetchmaintenacecount', views.FetchMaintenanceRequestCounts, name='FetchMaintenanceRequestCounts'),
    # REASSIGN DEVICE TO ANOTHER SUB STUDENT
    path('reassigndevice/<str:id>', views.ReassignDevice, name='ReassignDevice'),
    path('allunassigneddevices', views.UnassignedDevices, name='UnassignedDevices'),
    path('maintenanceissuetype', views.MaintenaceRequestIssueTypes, name='MaintenaceRequestIssueTypes'),
    # SEND SUB STUDENT EMAIL NOTIFICATION AFTER REGISTRATION
    # path('sendsubstudentemail', views.SendSubStudentEmailNotification, name='SendSubStudentEmailNotification'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




