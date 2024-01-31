from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import *
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from datetime import date
from django.db.models import Q
import json
from useronboard.models import SignupForm
from userarea.models import DeviceRegisterUpload

# Create your views here.


def AdminNavBar(request):
    return render(request, 'admingen.html')

def SuperAdminAccess(request):
    next = ""
    if request.GET:  
        next = request.GET['next']
        
    if request.method == 'POST':
        superadminmail = request.POST['superadminmail']
        password = request.POST['superadminpassword']
        try:
            user = User.objects.get(email=superadminmail)
            if user:
                userEmail = user.email
                # print(user.email)
        except:
            messages.error(request, 'The email address you entered is not registered. Please create an account to continue.')
            return redirect('SignUpPage')
        
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
    context = {'AllCompanyCount':AllCompanyCount, 'AllCompany':AllCompany, 'AllDevicesCount':AllDevicesCount, 'AllDevices':AllDevices,
    'AllFaultyDevicesCount':AllFaultyDevicesCount, 'AllHealthyDevicesCount':AllHealthyDevicesCount, 'AllMaintenanceRequestCount':AllMaintenanceRequestCount,
    
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


