from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import *
from userarea.models import CompanyFaultyDevices
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from datetime import date
from django.db.models import Q
import json
from useronboard.models import SignupForm
from userarea.models import DeviceRegisterUpload
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
        password = request.POST['superadminpassword']
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
                return redirect('SuperAdminDashboard')
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
    AllMaintenanceRequest = DeviceRegisterUpload.objects.filter(devicestatus = 'Working')
    AllMaintenanceRequestCount = AllMaintenanceRequest.count()
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
    FebHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Feb'))
    MarHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Mar'))
    AprHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Apr'))
    MayHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'May'))
    JunHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Jun'))
    JulHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Jul'))
    AugHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Aug'))
    SeptHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Sep'))
    OctHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Oct'))
    NovHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Nov'))
    DecHealthyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(registeredMonth = 'Dec'))
    
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
    }
    return render(request, 'dhmsadminboard/itsadashboard.html', context)


def AllDevices(request):
    return render(request, 'dhmsadminboard/devices.html')


def AdminMaintenance(request):
    return render(request, 'dhmsadminboard/superadminmaint.html')


def ITPartners(request):
    return render(request, 'dhmsadminboard/partners.html')


def SuperAdminReports(request):
    return render(request, 'dhmsadminboard/superreports.html')


def SuperAdminSettings(request):
    return render(request, 'dhmsadminboard/supersettings.html')


def Organizations(request):
    return render(request, 'dhmsadminboard/organizations.html')


def AdminLogout(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('SuperAdminAccess')




