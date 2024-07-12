from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import *
from userarea.models import CompanyFaultyDevices
from useronboard.models import SignupForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from datetime import date
from django.db.models import Q
import json
from useronboard.models import SignupForm
from userarea.models import *
from django.utils.crypto import get_random_string

# Create your views here.


def AdminNavBar(request):
    return render(request, 'admingen.html')


def SuperAdminAccessSignup(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        adminaccesslevel = request.POST['adminaccesslevel']
        UniqueID = 'admin' + '-' +  get_random_string(length=10)
        # address = request.POST['address']
        password = request.POST['password']
        rtpassword = request.POST['rtpassword']
        
        
        if not request.POST['adminaccesslevel']:
            messages.success(request, 'Registration Failed: Select an access level')
            return redirect('SuperAdminAccessSignup')

        if not request.POST['firstname']:
            messages.success(request, 'Registration Failed: Enter A First name')
            return redirect('SuperAdminAccessSignup')
        
        if not request.POST['lastname']:
            messages.success(request, 'Registration Failed: Enter A Last name')


        if (password != rtpassword):
            messages.error(request, 'Passwords Do Not Match!')
            return redirect('SuperAdminAccessSignup')

        data = SuperAdminsModel.objects.filter(email=email)
        # UserData = User.objects.filter(username=companyname)
        UserDataCheckEmail = User.objects.filter(email=email)
        if data:
            messages.error(request, 'Sorry, Email Address Is Already Taken.')
            return redirect('SuperAdminAccessSignup')

        elif UserDataCheckEmail:
            messages.error(request, 'Sorry, Email Address Is Already Taken, Please Use A Unique Email Address')
            return redirect('SuperAdminAccessSignup')
            
        else:
            form = SuperAdminsModel(firstname = firstname, lastname = lastname,  email=email, UniqueID = UniqueID, adminaccesslevel=adminaccesslevel, password=password)
            user = User.objects.create_user(username = email, email=email, password=password, last_name=lastname, first_name=firstname)
            form.save()
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            user.save()
            # activateEmail(request, user, email)
            # try:
            #     activateEmail(request, user, email)
            # except:
            #     print('Registration mail was not sent successfully')
            print('Admin registration was successfull. Login to continue')
            return redirect('SuperAdminAccess')
    return render(request, 'dhmsadminboard/superadminsignup.html')


def SuperAdminAccess(request):
    next = ""
    if request.GET:  
        next = request.GET['next']
        
    if request.method == 'POST':
        superadminmail = request.POST['superadminmail']
        # password = request.POST['superadminpassword']
        password = 'superadminpass121090890dhms'
        try:
            user = User.objects.get(email=superadminmail)
            useravailable = SuperAdminsModel.objects.get(email=superadminmail)
            if user:
                userEmail = user.email
                # print(user.email)
            if useravailable:
                pass
            else:
                messages.error(request, 'No admin account is tied to this email address.')
                return redirect('SuperAdminAccess')
                
        except:
            messages.error(request, 'The email address or password is incorrect. Kindly confirm and try again.')
            return redirect('SuperAdminAccess')
        
        user = authenticate(request, username=user, password=password)
        # LoginStatus.objects.create(user = user, email = superadminmail, status = 'Online')

        if user is not None:
            login(request, user)
            try:
                # notifyLoginEmail(request, user, superadminmail)
                pass
            except:
                pass
            if next == "":
                return redirect('SuperAdminSwitcher')
            else:
                return HttpResponseRedirect(next)
                
            # try:
            #     notifyLoginEmail(request, user, superadminmail)
            # except:
            #     pass
            # return redirect('SuperAdminDashboard')

        else:
            # print(error)
            messages.error(request, 'Login Failed: Please Try Again!!')
            return render(request, 'dhmsadminboard/superadminlogin.html')
    
    return render(request, 'dhmsadminboard/superadminlogin.html')


@login_required(login_url='SuperAdminAccess')
def SuperAdminSwitcher(request):
    return render(request, 'dhmsadminboard/superadminswitcher.html')


@login_required(login_url='SuperAdminAccess')
def SuperAdminDashboard(request):
    AllCompany = SignupForm.objects.all()
    AllCompanyCount = AllCompany.count()
    AllDevices = DeviceRegisterUpload.objects.all()
    AllDevicesCount = AllDevices.count()
    AllFaultyDevices = DeviceRegisterUpload.objects.filter(devicestatus = 'Faulty')
    AllFaultyDevicesCount = AllFaultyDevices.count()
    AllHealthyDevices = DeviceRegisterUpload.objects.filter(devicestatus = 'Working')
    AllHealthyDevicesCount = AllHealthyDevices.count()
    print('AllHealthyDevicesCount')
    # print(AllHealthyDevicesCount)
    AllMaintenanceRequest = MaintenanceRequest.objects.all()
    AllMaintenanceRequestCount = AllMaintenanceRequest.count()
    TopFourStaffMembers = StaffDataSet.objects.all()[:4]
    
    AllCompanyForData = SignupForm.objects.all()    
    LatestCompanyData = AllCompanyForData[0:1].values_list('companyUniqueID', flat=True)
    LatestCompanyDate1 = SignupForm.objects.get(companyUniqueID = LatestCompanyData)
    LatestCompanyDataCount = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = LatestCompanyData).count()
    
    SecondLatestDevData = AllCompanyForData[1:2].values_list('companyUniqueID', flat=True)
    SecondLatestDevData1 = SignupForm.objects.get(companyUniqueID = SecondLatestDevData)
    SecondLatestDevDataCount = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = SecondLatestDevData).count()
    
    ThirdLatestDevData = AllCompanyForData[2:3].values_list('companyUniqueID', flat=True)
    if ThirdLatestDevData:
        ThirdLatestDevData1 = SignupForm.objects.get(companyUniqueID = ThirdLatestDevData)
        ThirdLatestDevDataCount = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = ThirdLatestDevData).count()
    else:
        ThirdLatestDevData1 = 'None Device'
        ThirdLatestDevDataCount = 0
    
    FouthLatestDevData = AllCompanyForData[3:4].values_list('companyUniqueID', flat=True)
    if FouthLatestDevData:
        FouthLatestDevData1 = SignupForm.objects.get(companyUniqueID = FouthLatestDevData)
        FouthLatestDevDataCount = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = FouthLatestDevData).count()
    else:
        FouthLatestDevData1 = 'None Device'
        FouthLatestDevDataCount = 0
        
    
    LatestMaintenanceReqs = MaintenanceRequest.objects.all()[0:4]
    
    
    # FifthLatestDevData = AllCompanyForData[4:5].values_list('companyUniqueID', flat=True)
    # FifthLatestDevData1 = SignupForm.objects.get(companyUniqueID = FifthLatestDevData)
    # FifthLatestDevDataCount = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = FifthLatestDevData).count()
    
    # 
    
    JanDevices = CompanyFaultyDevices.objects.filter(month = 'Jan')
    FebDevices = CompanyFaultyDevices.objects.filter(month = 'Feb')
    MarDevices = CompanyFaultyDevices.objects.filter(month = 'Mar')
    AprDevices = CompanyFaultyDevices.objects.filter(month = 'Apr')
    MayDevices = CompanyFaultyDevices.objects.filter(month = 'May')
    JunDevices = CompanyFaultyDevices.objects.filter(month = 'Jun')
    JulDevices = CompanyFaultyDevices.objects.filter(month = 'Jul')
    AugDevices = CompanyFaultyDevices.objects.filter(month = 'Aug')
    SeptDevices = CompanyFaultyDevices.objects.filter(month = 'Sep')
    OctDevices = CompanyFaultyDevices.objects.filter(month = 'Oct')
    NovDevices = CompanyFaultyDevices.objects.filter(month = 'Nov')
    DecDevices = CompanyFaultyDevices.objects.filter(month = 'Dec')
    
    # 
    
    # 
    
    JanHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Jan'))
    # print(JanHealthyDevices.count())
    FebHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Feb'))
    MarHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Mar'))
    AprHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Apr'))
    MayHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'May'))
    JunHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Jun'))
    JulHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Jul'))
    AugHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Aug'))
    SeptHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Sep'))
    OctHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Oct'))
    print('Healthy Devices')
    NovHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Nov'))
    DecHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Dec'))
    print(DecHealthyDevices.count())
    
    # 
    context = {'AllCompanyCount':AllCompanyCount, 'AllCompany':AllCompany, 'AllDevicesCount':AllDevicesCount, 'AllDevices':AllDevices,
    'AllFaultyDevicesCount':AllFaultyDevicesCount, 'AllHealthyDevicesCount':AllHealthyDevicesCount, 'AllMaintenanceRequestCount':AllMaintenanceRequestCount,
    'JanDevices':JanDevices, 'FebDevices':FebDevices, 'AugDevices':AugDevices, 'SeptDevices':SeptDevices,
    'OctDevices':OctDevices, 'NovDevices':NovDevices, 'DecDevices':DecDevices, 'MarDevices':MarDevices, 
    'AprDevices':AprDevices, 'MayDevices':MayDevices,'JunDevices':JunDevices, 'JulDevices':JulDevices,
    # 
    'JanHealthyDevices':JanHealthyDevices, 'FebHealthyDevices':FebHealthyDevices, 'AugHealthyDevices':AugHealthyDevices, 'SeptHealthyDevices':SeptHealthyDevices,
    'OctHealthyDevices':OctHealthyDevices, 'NovHealthyDevices':NovHealthyDevices, 'DecHealthyDevices':DecHealthyDevices, 'MarHealthyDevices':MarHealthyDevices, 
    'AprHealthyDevices':AprHealthyDevices, 'MayHealthyDevices':MayHealthyDevices,'JunHealthyDevices':JunHealthyDevices, 'JulHealthyDevices':JulHealthyDevices,
    'LatestCompanyData':LatestCompanyData, 'LatestCompanyDate1':LatestCompanyDate1, 'LatestCompanyDataCount':LatestCompanyDataCount,
    'SecondLatestDevDataCount':SecondLatestDevDataCount, 'ThirdLatestDevData1':ThirdLatestDevData1, 'ThirdLatestDevDataCount':ThirdLatestDevDataCount,
    'FouthLatestDevData1':FouthLatestDevData1, 'FouthLatestDevDataCount':FouthLatestDevDataCount, 'LatestMaintenanceReqs':LatestMaintenanceReqs,
    'FouthLatestDevDataCount':FouthLatestDevDataCount, 'SecondLatestDevData1':SecondLatestDevData1, 'TopFourStaffMembers':TopFourStaffMembers,
    }
    return render(request, 'dhmsadminboard/itsadashboard.html', context)


def AllDevices(request):
    AllDevices = DeviceRegisterUpload.objects.all()
    AllOrgs = SignupForm.objects.all()
    AllDevicesCount = AllDevices.count()
    AllFaultyDevices = DeviceRegisterUpload.objects.filter(devicestatus = 'Faulty')
    AllFaultyDevicesCount = AllFaultyDevices.count()
    AllHealthyDevices = DeviceRegisterUpload.objects.filter(devicestatus = 'Working')
    AllHealthyDevicesCount = AllHealthyDevices.count()
    AllMaintenanceRequest = MaintenanceRequest.objects.all()
    AllMaintenanceRequestCount = AllMaintenanceRequest.count()
    AllOrgFaultyDevices = DeviceRegisterUpload.objects.filter(devicestatus = 'Faulty')
    AllOrgCriticalDevices = DeviceRegisterUpload.objects.filter(devicestatus = 'Critical')
    AllOrgCriticalDevicesCount =AllOrgCriticalDevices.count()
    AllOrgFaultyDevicesCount = AllOrgFaultyDevices.count()
    AllOrgFaultyDevicesCountMain = int(AllOrgFaultyDevicesCount) + int(AllOrgCriticalDevicesCount)
    context = {'AllDevicesCount':AllDevicesCount, 'AllFaultyDevicesCount':AllFaultyDevicesCount, 'AllHealthyDevicesCount':AllHealthyDevicesCount,
               'AllMaintenanceRequestCount':AllMaintenanceRequestCount, 'AllOrgFaultyDevicesCountMain':AllOrgFaultyDevicesCountMain,
               'AllDevices':AllDevices, 'AllOrgs':AllOrgs}
    return render(request, 'dhmsadminboard/devices.html', context)


def AdminMaintenance(request):
    AllMaintenanceRequest = MaintenanceRequest.objects.all()
    AllCompany = SignupForm.objects.all()
    AllMaintenanceRequestCount = AllMaintenanceRequest.count()
    PendingMaintenanceRequest = MaintenanceRequest.objects.filter(MaintainStatus = 'Pending')
    PendingMaintenanceRequestCount = PendingMaintenanceRequest.count()
    CompletedMaintenanceRequest = MaintenanceRequest.objects.filter(MaintainStatus = 'Completed')
    CompletedMaintenanceRequestCount = CompletedMaintenanceRequest.count()
    CancelledMaintenanceRequest = MaintenanceRequest.objects.filter(MaintainStatus = 'Cancelled')
    CancelledMaintenanceRequestCount = CancelledMaintenanceRequest.count()
    OngoingMaintenanceRequest = MaintenanceRequest.objects.filter(MaintainStatus = 'Ongoing')
    OngoingMaintenanceRequestCount = OngoingMaintenanceRequest.count()
    context = {'AllMaintenanceRequest':AllMaintenanceRequest, 'AllMaintenanceRequestCount':AllMaintenanceRequestCount, 'PendingMaintenanceRequestCount':PendingMaintenanceRequestCount,
               'CompletedMaintenanceRequestCount':CompletedMaintenanceRequestCount, 'CancelledMaintenanceRequestCount':CancelledMaintenanceRequestCount,
               'OngoingMaintenanceRequestCount':OngoingMaintenanceRequestCount, 'AllCompany':AllCompany
               }
    return render(request, 'dhmsadminboard/superadminmaint.html', context)


def ITPartners(request):
    return render(request, 'dhmsadminboard/partners.html')


def SuperAdminReports(request):
    return render(request, 'dhmsadminboard/superreports.html')


def SuperAdminSettings(request):
    return render(request, 'dhmsadminboard/supersettings.html')



def OrganizationsDetails(request, pk):
    SelectedOrg = SignupForm.objects.get(companyUniqueID = pk)
    AllOrgDevices = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = pk)
    AllOrgDevicesCount = AllOrgDevices.count()
    AllOrgStaff = StaffDataSet.objects.filter(CompanyUniqueCode = pk)
    AllOrgStaffCount = AllOrgStaff.count()    
    AllOrgHealthyDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = pk) & Q(devicestatus = 'Working'))
    AllOrgHealthyDevicesCount = AllOrgHealthyDevices.count()
    AllOrgFaultyDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = pk) & Q(devicestatus = 'Faulty'))
    AllOrgCriticalDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = pk) & Q(devicestatus = 'Critical'))
    AllOrgCriticalDevicesCount =AllOrgCriticalDevices.count()
    AllOrgFaultyDevicesCount = AllOrgFaultyDevices.count()
    AllOrgFaultyDevicesCountMain = int(AllOrgFaultyDevicesCount) + int(AllOrgCriticalDevicesCount)
    
    AllOrgMainteDevices = MaintenanceRequest.objects.filter(CompanyUniqueCode = pk)
    AllOrgMainteDevicesCount =AllOrgMainteDevices.count()
    
    context = {'SelectedOrg':SelectedOrg, 'AllOrgDevices':AllOrgDevices, 'AllOrgDevicesCount':AllOrgDevicesCount, 
            'AllOrgStaffCount':AllOrgStaffCount, 'AllOrgStaff':AllOrgStaff, 'AllOrgHealthyDevicesCount':AllOrgHealthyDevicesCount,
            'AllOrgFaultyDevicesCountMain':AllOrgFaultyDevicesCountMain, 'AllOrgMainteDevicesCount':AllOrgMainteDevicesCount}
    return render(request, 'dhmsadminboard/superorgdetails.html', context)



def Organizations(request):
    AllOrganizations = SignupForm.objects.all()
    AllDevices = DeviceRegisterUpload.objects.all()
    AllStaffMembers = StaffDataSet.objects.all()
    AllOrganizationsCount = AllOrganizations.count()    
    context = {'AllOrganizations':AllOrganizations, 'AllOrganizationsCount':AllOrganizationsCount, 'AllDevices':AllDevices, 'AllStaffMembers':AllStaffMembers}
    return render(request, 'dhmsadminboard/organizations.html', context)


def AdminLogout(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('SuperAdminAccess')








