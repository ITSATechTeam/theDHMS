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


# 
from getmac import get_mac_address as gma
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)

import wmi
c = wmi.WMI()    
my_system = c.Win32_ComputerSystem()[0]


import platform
os_name = platform.system()


# Create your views here.
def UserReg(request):
    ThisFamilyId = 'Family-' + get_random_string(length=5)
    if request.method == 'POST' and 'fullname' in request.POST:
        print('fam dhms submitted')
        email = request.POST['familyemail']
        fullname = request.POST['fullname']
        password = request.POST['password']
        familyUniqueID = ThisFamilyId

        if not request.POST['familyemail']:
            messages.success(request, 'Registration Failed: Kindly provide a valid email address.')
            return redirect('UserReg')

        elif not request.POST['fullname']:
            messages.success(request, 'Registration Failed: Kindly provide a valid full name.')
            return redirect('UserReg')

        elif not request.POST['password']:
            messages.success(request, 'Registration Failed: Kindly enter a password.')
            return redirect('UserReg')

        checkfullname = Familyregister.objects.filter(fullname=fullname)
        UserData = User.objects.filter(username=fullname)
        UserDataCheckEmail = User.objects.filter(email=email)
        if checkfullname or UserData:
            messages.error(request, 'Sorry, Full Name Is Already Taken, Please Use Another Full Name For Your Family')
            return redirect('UserReg')

        elif UserDataCheckEmail:
            messages.error(request, 'Sorry, Email Address Is Already Taken, Please Use A Unique Email Address')
            return redirect('UserReg')
        
        else:
            messages.success(request, 'Your family is successfully registered')
            regFamily = User.objects.create_user(username = fullname, email = email, first_name = fullname, password = password, last_name = familyUniqueID)
            FamilyregisterMain = Familyregister(email = email, fullname = fullname, password = password, familyUniqueID = familyUniqueID)
            regFamily.save()
            FamilyregisterMain.save()
            return redirect('FamilyDHMSDashboard')


    return render(request, 'familydhmsapp/signinpage.html')


def UserLogin(request):
    next = ""

    if request.GET:  
        next = request.GET['next']
        
    if request.method == 'POST':
        familyuser = request.POST['familyemail']
        password = request.POST['password']

        try:
            user = User.objects.get(email=familyuser)
            if user:
                userEmail = user.email
                # user = authenticate(request, username=user, password=password)
            else:
                messages.error(request, 'The email address you entered is not registered. Please create an account to continue.')
                return redirect('UserReg')

        except:
            messages.error(request, 'The email address you entered is not registered. Please create an account to continue.')
            return redirect('UserReg')
        
        user = authenticate(request, username=user, password=password)

        if user is not None:
            login(request, user)
            if next == "":
                return redirect('FamilyDHMSDashboard')
            else:
                return HttpResponseRedirect(next)

        else:
            messages.error(request, 'Login Failed: Please Try Again!!')

    return render(request, 'familydhmsapp/loginpage.html')

@login_required(login_url='UserLogin')
def FamilyDHMSDashboard(request):
    DeviceHostName = hostname
    DeviceMacAddress = gma()
    DeviceIP = ip_address
    DeviceManufacturter = my_system.Manufacturer
    DeviceSystemModel = my_system. Model
    DeviceName = my_system.Name
    DeviceNumOfProcessor = my_system.NumberOfProcessors
    DeviceSystemType = my_system.SystemType
    DeviceSystemFamily = my_system.SystemFamily
    DeviceOS = os_name

    if request.method == 'POST' and 'deviceyearofpurchase' in request.POST:
        print('deviceyearofpurchase triggered successfully')
        today = date.today()                                        
        dateForWeekNumber = datetime.today()
        weekNumber = dateForWeekNumber.isocalendar().week
        devicetype = request.POST['devicetype']
        devicebrand = request.POST['devicebrand']
        deviceOS = request.POST['deviceos']
        devicelocation = request.POST['devicelocation']
        deviceyearofpurchase = request.POST['deviceyearofpurchase']
        FamilyUniqueCode = request.POST['FamilyUniqueCode']
        devicename = request.POST['devicename']
        devicemacaddress = request.POST['devicemacaddress']
        deviceipaddress = request.POST['deviceip']
        Reqfamilyadmin = request.user
        FamilyUniqueCode = request.user.last_name
        uniqueId = 'Family_Device-'  + get_random_string(length=8)
        dateForWeekNumber = datetime.today()
        
        if not request.POST['devicetype']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Type.")
            return redirect('FamilyDHMSDashboard')
        
        if not request.POST['devicebrand']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Brand.")
            return redirect('FamilyDHMSDashboard')
        
        if not request.POST['devicemacaddress']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's MAC Address.")
            return redirect('FamilyDHMSDashboard')
        
        if not request.POST['deviceip']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's IP Address.")
            return redirect('FamilyDHMSDashboard')

        
        if request.POST['deviceyearofpurchase']:
            depreciateRate = 2023 - int(request.POST['deviceyearofpurchase'])
            # calc depreciateRateReal from depreciateRate below:
            if depreciateRate <= 0:
                depreciateRateReal = '100%'
            elif depreciateRate == 1:
                depreciateRateReal = '75%'
            elif depreciateRate == 2:
                depreciateRateReal = '50%'
            elif depreciateRate == 3:
                depreciateRateReal = '25%'
            elif depreciateRate >= 4:
                depreciateRateReal = '0%'
            else:
                depreciateRateReal = 'Nil'
        else:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Year Of Purchase.")
            return redirect('FamilyDHMSDashboard')

        FamilyDeviceRegForm = FamilyDeviceReg(user = Reqfamilyadmin, devicetype = devicetype, devicebrand = devicebrand, deviceOS = deviceOS,
        deviceyearofpurchase = deviceyearofpurchase, devicelocation = devicelocation, devicename = devicename, devicemacaddress = devicemacaddress,
        deviceipaddress = deviceipaddress, FamilyUniqueCode = FamilyUniqueCode, devicedepreciationrate = depreciateRateReal, deviceid = uniqueId,
        savetimedata = today.strftime("%B %d, %Y"), registeredMonth = today.strftime("%b"), weekNumberSaved = weekNumber)
        FamilyDeviceRegForm.save()
        messages.error(request, "Device saved successfully.")
        return redirect('FamilyDHMSDashboard')

        try:
            FamilyDeviceRegForm = FamilyDeviceReg(user = Reqfamilyadmin, devicetype = devicetype, devicebrand = devicebrand, deviceOS = deviceOS,
            deviceyearofpurchase = deviceyearofpurchase, devicelocation = devicelocation, devicename = devicename, devicemacaddress = devicemacaddress,
            deviceipaddress = deviceipaddress, FamilyUniqueCode = FamilyUniqueCode, devicedepreciationrate = depreciateRateReal, deviceid = uniqueId,
            savetimedata = today.strftime("%B %d, %Y"), registeredMonth = today.strftime("%b"), weekNumberSaved = weekNumber)
            FamilyDeviceRegForm.save()
            messages.error(request, "Device registered successfully.")
            return redirect('FamilyDHMSDashboard')
        except:
            messages.error(request, "An error occured while trying to save this device, please try again.")
            return redirect('FamilyDHMSDashboard')



        # REGISTER YOUR DEVICE SELF SET UP STARTS HERE

    if request.method == 'POST' and 'DeviceHostName_Self' in request.POST:
        today = date.today()                                        
        dateForWeekNumber = datetime.today()
        weekNumber = dateForWeekNumber.isocalendar().week
        DeviceHostName_Self = request.POST['DeviceHostName_Self']
        DeviceMacAddress_Self = request.POST['DeviceMacAddress_Self']
        DeviceIP_Self = request.POST['DeviceIP_Self']
        DeviceName_Self = request.POST['DeviceName_Self']
        DeviceManufacturter_Self = request.POST['DeviceManufacturter_Self']
        DeviceSystemModel_Self = request.POST['DeviceSystemModel_Self']
        DeviceNumOfProcessor_Self = request.POST['DeviceNumOfProcessor_Self']
        DeviceSystemType_Self = request.POST['DeviceSystemType_Self']
        DeviceOS_Self = request.POST['DeviceOS_Self']
        devicelocation_Self = request.POST['devicelocation_Self']
        Deviceyearofpurchase_Self = request.POST['Deviceyearofpurchase_Self']

        uniqueId = 'Family_Device-'  + get_random_string(length=8)
        dateForWeekNumber = datetime.today()
        
        if request.POST['Deviceyearofpurchase_Self']:
            depreciateRate = 2023 - int(request.POST['Deviceyearofpurchase_Self'])
            # calc depreciateRateReal from depreciateRate below:
            if depreciateRate <= 0:
                depreciateRateReal_self = '100%'
            elif depreciateRate == 1:
                depreciateRateReal_self = '75%'
            elif depreciateRate == 2:
                depreciateRateReal_self = '50%'
            elif depreciateRate == 3:
                depreciateRateReal_self = '25%'
            elif depreciateRate >= 4:
                depreciateRateReal_self = '0%'
            else:
                depreciateRateReal_self = 'Nil'
        else:
            depreciateRateReal_self = 'Nil'

        try:
            FamilyDeviceRegForm = FamilyDeviceReg(user = request.user, devicetype = DeviceSystemType_Self, devicebrand = DeviceManufacturter_Self, deviceOS = DeviceOS_Self,
            deviceyearofpurchase = Deviceyearofpurchase_Self, devicelocation = devicelocation_Self, devicename = DeviceHostName_Self, devicemacaddress = DeviceMacAddress_Self,
            deviceipaddress = DeviceIP_Self, FamilyUniqueCode = request.user.last_name, devicedepreciationrate = depreciateRateReal_self, deviceid = uniqueId,
            savetimedata = today.strftime("%B %d, %Y"), registeredMonth = today.strftime("%b"), weekNumberSaved = weekNumber, devicemodel = DeviceSystemModel_Self)
            FamilyDeviceRegForm.save()
            messages.error(request, "Device Registered Successfully.")
            return redirect('FamilyDHMSDashboard')

        except:
            messages.error(request, "An error occured while trying to save this device, please try again.")
            return redirect('FamilyDHMSDashboard')
        
    
    allfamilymembers = FamilyMemberReg.objects.filter(user = request.user)
    allfamilymembersCount = allfamilymembers.count()
    
    allFamilyDeviceReg = FamilyDeviceReg.objects.filter(user = request.user)
    allFamilyDeviceRegCount = allFamilyDeviceReg.count()

    context = {'DeviceHostName':DeviceHostName, 'DeviceMacAddress':DeviceMacAddress, 'DeviceIP':DeviceIP, 'DeviceManufacturter':DeviceManufacturter,
    'DeviceSystemModel':DeviceSystemModel, 'DeviceName':DeviceName, 'DeviceNumOfProcessor':DeviceNumOfProcessor, 'DeviceSystemType':DeviceSystemType, 
    'DeviceSystemFamily': DeviceSystemFamily, 'DeviceOS':DeviceOS, 'allfamilymembersCount':allfamilymembersCount, 
    'allFamilyDeviceRegCount':allFamilyDeviceRegCount}

    return render(request, 'familydhmsapp/familydashboard.html', context)



def FamilyInventory(request):
    return render(request, 'familydhmsapp/familyinventory.html')


def FamilyMaintenance(request):
    return render(request, 'familydhmsapp/familymaintain.html')


def FamilyAnalytics(request):
    return render(request, 'familydhmsapp/familyanalytics.html')


def FamilySupport(request):
    return render(request, 'familydhmsapp/familysupport.html')


def FamilySettings(request):
    return render(request, 'familydhmsapp/familysettings.html')

@login_required(login_url='UserLogin')
def FamilyMembers(request):
    if request.method == 'POST' and 'email' in request.POST:
        fullname = request.POST['fullname']
        email = request.POST['email']
        memberid = 'FM-'  + get_random_string(length=5)

        if not request.POST['fullname']:
            messages.error(request, 'Registration Failed: Kindly provide a full name for this family member.')
            return redirect('FamilyMembers')

        if not request.POST['email']:
            messages.error(request, 'Registration Failed: Kindly provide an email address for this family member.')
            return redirect('FamilyMembers')

        checkemail = User.objects.filter(email = request.POST['email'])
        checkfullname = User.objects.filter(first_name = request.POST['fullname'])
        checkfamilyemail = FamilyMemberReg.objects.filter(memberemail = request.POST['email'])
        checkfamilyfullname = FamilyMemberReg.objects.filter(memberfullname = request.POST['fullname'])
        if (checkemail):
            messages.error(request, 'Registration Failed: Email address is already registered to an existing user.')
            return redirect('FamilyMembers')

        if (checkfullname):
            messages.error(request, 'Registration Failed: Full name is already registered to an existing user.')
            return redirect('FamilyMembers')

        if (checkfamilyemail):
            messages.error(request, 'Registration Failed: Email address is already registered to an existing user.')
            return redirect('FamilyMembers')

        if (checkfamilyfullname):
            messages.error(request, 'Registration Failed: Full name is already registered to an existing user.')
            return redirect('FamilyMembers')

        familymemberform = FamilyMemberReg(user = request.user, memberfullname = fullname, memberemail = email, memberid = memberid, familyid = request.user.last_name)

        try:
            familymemberform.save()
            messages.success(request, "You registered a family member successfully.")
            return redirect('FamilyMembers')
        except:
            messages.error(request, "An error occured while saving family member. Kindly try again.")
            return redirect('FamilyMembers')
    allfamilymembers = FamilyMemberReg.objects.filter(user = request.user)
    allfamilymembersCount = allfamilymembers.count()
    context = {'allfamilymembers':allfamilymembers, 'allfamilymembersCount':allfamilymembersCount}
    return render(request, 'familydhmsapp/familymember.html', context)


def FamilyLogout(request):
    logout(request)
    messages.error(request, 'Logout Successfull.')
    return redirect('UserLogin')


# def FinDetails(request):










