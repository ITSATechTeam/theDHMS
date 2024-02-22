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

# 
from getmac import get_mac_address as gma
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)


import platform
os_name = platform.system()
my_system = platform.uname()

@login_required(login_url='UserLogin')
def Famnavbar(request):
    return render(request, 'famgeneral.html')

# Create your views here.
def UserReg(request):
    ThisFamilyId = 'Family-' + get_random_string(length=5)
    if request.method == 'POST' and 'fullname' in request.POST:
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

        findemailinrec = Familyregister.objects.filter(email=familyuser)
        findemailinrecgen = User.objects.filter(email=familyuser)
        print(findemailinrecgen)
        if findemailinrec:
            try:
                user = User.objects.get(email=familyuser)
                print(user)
                if user:
                    userEmail = user.email
                    # messages.error(request, 'The email address you entered is already registered on the DHMS. Please enter a unique email address.')
                    # return redirect('UserLogin')

                else:
                    messages.error(request, 'The email address you entered is not registered. Please create an account to continueeee.')
                    return redirect('UserReg')

            except:
                messages.error(request, 'An error occured during validation. Please try again.')
                return redirect('UserLogin')
            
            user = authenticate(request, username=user, password=password)

            if user is not None:
                login(request, user)
                if next == "":
                    return redirect('FamilyDHMSDashboard')
                else:
                    return HttpResponseRedirect(next)

            else:
                messages.error(request, 'Login Failed: Please Try Again!!')
                
        else:
            messages.error(request, 'The email address you entered is not registered. Please create an account to continue...')
            return redirect('UserReg')

    return render(request, 'familydhmsapp/loginpage.html')

import requests
@login_required(login_url='UserLogin')
def FamilyDHMSDashboard(request):
    # GET DEVICE INFO
    if request.user_agent.is_mobile:
        device_type = "Mobile"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    if request.user_agent.is_pc:
        device_type = "PC"    
    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string
    Device_IP_Self = request.META.get('REMOTE_ADDR')
    # 
    if request.method == 'POST' and 'deviceyearofpurchase' in request.POST:
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
        devicestatus = request.POST['devicestatus']
        deviceUserID = request.POST['deviceUserID']
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

        try:
            if request.POST['devicestatus'] == 'Faulty' or request.POST['devicestatus'] == 'Critical':
                FaultyDevicesTrendForm = FaultyDevicesTrend(user = request.user, deviceID = uniqueId, month =  today.strftime("%b"), 
                year = today.strftime("%B %d, %Y"), FamilyUniqueCode = request.user.last_name)

            if request.POST['deviceUserID']:
                FindDeviceUserEmail = FamilyMemberReg.objects.filter(Q(user = request.user) & Q(memberid = request.POST['deviceUserID']))
                FindDeviceUserEmailMain = FindDeviceUserEmail.values_list('memberemail', flat=True)
                FindDeviceUserFullname = FamilyMemberReg.objects.filter(Q(user = request.user) & Q(memberid = request.POST['deviceUserID']))
                FindDeviceUserFullnameMain = FindDeviceUserFullname.values_list('memberfullname', flat=True)
                
                FamilyDeviceRegForm = FamilyDeviceReg(user = Reqfamilyadmin, devicestatus = devicestatus, devicetype = devicetype, devicebrand = devicebrand, deviceOS = deviceOS,
                deviceyearofpurchase = deviceyearofpurchase, devicelocation = devicelocation, devicename = devicename, devicemacaddress = devicemacaddress,
                deviceipaddress = deviceipaddress, FamilyUniqueCode = FamilyUniqueCode, devicedepreciationrate = depreciateRateReal, deviceid = uniqueId,
                savetimedata = today.strftime("%B %d, %Y"), registeredMonth = today.strftime("%b"), weekNumberSaved = weekNumber, deviceUserID = deviceUserID,
                deviceuseremail = FindDeviceUserEmailMain, deviceuserfullname = FindDeviceUserFullnameMain)
                FamilyDeviceRegForm.save()
                FaultyDevicesTrendForm.save()
                messages.error(request, "Device registered successfully, and has been assigned.")
                return redirect('FamilyDHMSDashboard')
            
            else:
                FamilyDeviceRegForm = FamilyDeviceReg(user = Reqfamilyadmin, devicestatus = devicestatus, devicetype = devicetype, devicebrand = devicebrand, deviceOS = deviceOS,
                deviceyearofpurchase = deviceyearofpurchase, devicelocation = devicelocation, devicename = devicename, devicemacaddress = devicemacaddress,
                deviceipaddress = deviceipaddress, FamilyUniqueCode = FamilyUniqueCode, devicedepreciationrate = depreciateRateReal, deviceid = uniqueId,
                savetimedata = today.strftime("%B %d, %Y"), registeredMonth = today.strftime("%b"), weekNumberSaved = weekNumber)            
                FamilyDeviceRegForm.save()
                FaultyDevicesTrendForm.save()
                messages.error(request, "Device registered successfully.")
                return redirect('FamilyDHMSDashboard')

        except:
            messages.error(request, "An error occured while trying to save this device, please try again.")
            return redirect('FamilyDHMSDashboard')



        # REGISTER YOUR DEVICE SELF SET UP STARTS HERE

    if request.method == 'POST' and 'Device_IP_Self' in request.POST:
        today = date.today()
        dateForWeekNumber = datetime.today()
        weekNumber = dateForWeekNumber.isocalendar().week
        devicestatus = request.POST['devicestatus']
        DeviceName_Self = request.POST['DeviceName_Self']
        DeviceMacAddress_Self = request.POST['devicemacaddress_Self']
        DeviceIP_Self = request.POST['Device_IP_Self']
        BrowserType_Self = request.POST['BrowserType_Self']
        BrowserVersion_Self = request.POST['BrowserVersion_Self']
        DeviceSystemType_Self = request.POST['DeviceSystemType_Self']
        DeviceOSType_Self = request.POST['DeviceOSType_Self']
        DeviceOSVersion_Self = request.POST['DeviceOSVersion_Self']
        devicelocation_Self = request.POST['devicelocation_Self']
        Deviceyearofpurchase_Self = request.POST['Deviceyearofpurchase_Self']

        uniqueId = 'Family_Device-'+ get_random_string(length=8)
        dateForWeekNumber = datetime.today()
        
        # if not request.POST['DeviceName_Self']:
        #     messages.error(request, "Device uploaded failed. Kindly try again.")
        #     return redirect('FamilyDHMSDashboard')
        
        # if not request.POST['devicestatus']:
        #     messages.error(request, "Device uploaded failed. Kindly Provide Your Device Health Status.")
        #     return redirect('FamilyDHMSDashboard')
        
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
            depreciateRateReal_self = '0%'

        try:
            if request.POST['devicestatus'] == 'Faulty' or request.POST['devicestatus'] == 'Critical':
                FaultyDevicesTrendForm = FaultyDevicesTrend(user = request.user, deviceID = uniqueId, month =  today.strftime("%b"), 
                year = today.strftime("%B %d, %Y"), FamilyUniqueCode = request.user.last_name)
                FaultyDevicesTrendForm.save()

            FamilyDeviceRegForm = FamilyDeviceReg(user = request.user, devicetype = DeviceSystemType_Self, deviceOS = DeviceOSType_Self,
            deviceyearofpurchase = Deviceyearofpurchase_Self, devicelocation = devicelocation_Self, devicename = DeviceName_Self, devicemacaddress = DeviceMacAddress_Self,
            deviceipaddress = DeviceIP_Self, FamilyUniqueCode = request.user.last_name, devicedepreciationrate = depreciateRateReal_self, deviceid = uniqueId,
            userbrowser = BrowserType_Self, userbrowserversion = BrowserVersion_Self, userOSVersion = DeviceOSVersion_Self, devicestatus = devicestatus,
            savetimedata = today.strftime("%B %d, %Y"), deviceuserfullname = request.user.first_name, deviceUserID = request.user.last_name, deviceuseremail = request.user.email,
            registeredMonth = today.strftime("%b"), weekNumberSaved = weekNumber)
            FamilyDeviceRegForm.save()
            messages.success(request, "Device Registered Successfully.")
            return redirect('FamilyDHMSDashboard')

        except:
            messages.error(request, "An error occured while trying to save this device, please try again.")
            return redirect('FamilyDHMSDashboard')
        
    
    allfamilymembers = FamilyMemberReg.objects.filter(user = request.user)
    allfamilymembersCount = allfamilymembers.count()
    
    allFamilyDeviceReg = FamilyDeviceReg.objects.filter(user = request.user)
    allFamilyDeviceRegCount = allFamilyDeviceReg.count()
    
    AllMaintenanceReqs = FamilyMaintainanceReq.objects.filter(user = request.user)
    AllMaintenanceReqsCount = AllMaintenanceReqs.count()
    
    AllFaultyDevices = FamilyDeviceReg.objects.filter(Q(user = request.user) & Q(devicestatus = 'Faulty'))
    AllFaultyDevicesCount = AllFaultyDevices.count()
    
    AllCriticalDevices = FamilyDeviceReg.objects.filter(Q(user = request.user) & Q(devicestatus = 'Critical'))
    AllCriticalDevicesCount = AllCriticalDevices.count()
    
    AllFaultyAndCritialDevices = AllFaultyDevicesCount + AllCriticalDevicesCount
    AllWorkingDevices = FamilyDeviceReg.objects.filter(Q(user = request.user) & Q(devicestatus = 'Working'))
    AllWorkingDevicesCount = AllWorkingDevices.count()


    allLaptopDevices = FamilyDeviceReg.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(devicetype = 'Laptop'))
    allPCDevices = FamilyDeviceReg.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(devicetype = 'PC'))
    allPCDevicesCount = allPCDevices.count()
    allLaptopDevicesCount = allLaptopDevices.count()
    allLaptopDevicesCountMain = allLaptopDevicesCount + allPCDevicesCount
    allDesktopDevices = FamilyDeviceReg.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(devicetype = 'Desktop'))
    allDesktopDevicesCount = allDesktopDevices.count()
    data = [allLaptopDevicesCountMain, allDesktopDevicesCount]
    labels = ['Laptops', 'Desktops']

    AllFaultyDevicesTrend = FaultyDevicesTrend.objects.filter(FamilyUniqueCode = request.user.last_name)
    JanDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'Jan'))
    FebDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'Feb'))
    MarDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'Mar'))
    AprDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'Apr'))
    MayDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'May'))
    JunDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'Jun'))
    JulDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'Jul'))
    AugDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'Aug'))
    SeptDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'Sep'))
    OctDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'Oct'))
    NovDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'Nov'))
    DecDevices = FaultyDevicesTrend.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(month = 'Dec'))

    #
    # AprDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Apr'))
    # AprDevices1 = AprDevices.count()
    # 


    context = {
    'AllMaintenanceReqsCount':AllMaintenanceReqsCount,
    'DeviceType':device_type,
    'BrowserType':browser_type, 
    'BrowserVersion':browser_version, 
    'DeviceOSType':os_type,
    'DeviceOSVersion':os_version, 
    'Device_IP_Self': Device_IP_Self,
    'allfamilymembers':allfamilymembers, 
    'allfamilymembersCount':allfamilymembersCount, 
    'allFamilyDeviceReg':allFamilyDeviceReg,
    'allFamilyDeviceRegCount':allFamilyDeviceRegCount,
    'AllFaultyDevicesTrend':AllFaultyDevicesTrend,
    'JanDevices':JanDevices,
    'FebDevices':FebDevices,
    'MarDevices':MarDevices,
    'AprDevices':AprDevices,
    'MayDevices':MayDevices,
    'JunDevices':JunDevices,
    'JulDevices':JulDevices,
    'AugDevices':AugDevices,
    'SeptDevices':SeptDevices,
    'OctDevices':OctDevices,
    'NovDevices':NovDevices,
    'DecDevices':DecDevices,
    'data':data,
    'labels':labels,
    'allLaptopDevicesCountMain':allLaptopDevicesCountMain,
    'allDesktopDevicesCount':allDesktopDevicesCount,
    'AllFaultyAndCritialDevices':AllFaultyAndCritialDevices,
    'AllWorkingDevicesCount':AllWorkingDevicesCount
    }

    return render(request, 'familydhmsapp/familydashboard.html', context)


@login_required(login_url='UserLogin')
def FamilyInventory(request):
    #     
    if request.method == 'POST' and 'FamilyUniqueCode' in request.POST:
        print('form triggered')
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
        devicestatus = request.POST['devicestatus']
        deviceUserID = request.POST['deviceUserID']
        deviceimage = request.FILES.get('device_images')
        Reqfamilyadmin = request.user
        FamilyUniqueCode = request.user.last_name
        uniqueId = 'Family_Device-'  + get_random_string(length=8)
        dateForWeekNumber = datetime.today()

        if deviceimage is not None:
            print('No device image')
        if not request.POST['devicetype']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Type.")
            return redirect('FamilyInventory')
        
        if not request.POST['devicebrand']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Brand.")
            return redirect('FamilyInventory')
        
        if not request.POST['devicemacaddress']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's MAC Address.")
            return redirect('FamilyInventory')
        
        if not request.POST['deviceip']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's IP Address.")
            return redirect('FamilyInventory')
        
        if not request.POST['deviceos']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Operating System(OS).")
            return redirect('FamilyInventory')
        
        if not request.POST['deviceip']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's IP Address.")
            return redirect('FamilyInventory')
        
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
            return redirect('FamilyInventory')      

        try:
            if request.POST['deviceUserID']:
                FindDeviceUserEmail = FamilyMemberReg.objects.filter(Q(user = request.user) & Q(memberid = request.POST['deviceUserID']))
                FindDeviceUserEmailMain = FindDeviceUserEmail.values_list('memberemail', flat=True)
                FindDeviceUserFullname = FamilyMemberReg.objects.filter(Q(user = request.user) & Q(memberid = request.POST['deviceUserID']))
                FindDeviceUserFullnameMain = FindDeviceUserFullname.values_list('memberfullname', flat=True)
                
                FamilyDeviceRegForm = FamilyDeviceReg(user = Reqfamilyadmin, devicestatus = devicestatus, devicetype = devicetype, devicebrand = devicebrand, deviceOS = deviceOS,
                deviceyearofpurchase = deviceyearofpurchase, devicelocation = devicelocation, devicename = devicename, devicemacaddress = devicemacaddress,
                deviceipaddress = deviceipaddress, FamilyUniqueCode = FamilyUniqueCode, devicedepreciationrate = depreciateRateReal, deviceid = uniqueId,
                savetimedata = today.strftime("%B %d, %Y"), registeredMonth = today.strftime("%b"), weekNumberSaved = weekNumber, deviceUserID = deviceUserID,
                deviceuseremail = FindDeviceUserEmailMain, deviceuserfullname = FindDeviceUserFullnameMain, deviceImageOne = deviceimage)
                # 
                if request.POST['devicestatus'] == 'Faulty' or request.POST['devicestatus'] == 'Critical':
                    FaultyDevicesTrendForm = FaultyDevicesTrend(user = request.user, deviceID = uniqueId, month =  today.strftime("%b"), 
                    year = today.strftime("%B %d, %Y"), FamilyUniqueCode = request.user.last_name)
                    FaultyDevicesTrendForm.save()

                FamilyDeviceRegForm.save()
                messages.error(request, "Device registered successfully.")
                return redirect('FamilyInventory')
            
            else:
                FamilyDeviceRegForm = FamilyDeviceReg(user = Reqfamilyadmin, devicestatus = devicestatus, devicetype = devicetype, devicebrand = devicebrand, deviceOS = deviceOS,
                deviceyearofpurchase = deviceyearofpurchase, devicelocation = devicelocation, devicename = devicename, devicemacaddress = devicemacaddress,
                deviceipaddress = deviceipaddress, FamilyUniqueCode = FamilyUniqueCode, devicedepreciationrate = depreciateRateReal, deviceid = uniqueId,
                savetimedata = today.strftime("%B %d, %Y"), registeredMonth = today.strftime("%b"), weekNumberSaved = weekNumber, deviceImageOne = deviceimage)            
                FamilyDeviceRegForm.save()
                FaultyDevicesTrendForm.save()
                messages.error(request, "Device registered successfully.")
                return redirect('FamilyInventory') 

        except:
            messages.error(request, "An error occured while trying to save this device, please try again.")
            return redirect('FamilyInventory')

    # 
    allfamilymembers = FamilyMemberReg.objects.filter(user = request.user)
    AllFamilyDevices = FamilyDeviceReg.objects.filter(user = request.user)
    AllFamilyDevicesCount = AllFamilyDevices.count()
    allLaptopDevices = FamilyDeviceReg.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(devicetype = 'Laptop'))
    allPCDevices = FamilyDeviceReg.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(devicetype = 'PC'))
    allPCDevicesCount = allPCDevices.count()
    allLaptopDevicesCount = allLaptopDevices.count()
    allLaptopDevicesCountMain = allLaptopDevicesCount + allPCDevicesCount
    allDesktopDevices = FamilyDeviceReg.objects.filter(Q(FamilyUniqueCode = request.user.last_name) & Q(devicetype = 'Desktop'))
    allDesktopDevicesCount = allDesktopDevices.count()
    
    AllFaultyDevices = FamilyDeviceReg.objects.filter(Q(user = request.user) & Q(devicestatus = 'Faulty'))
    AllFaultyDevicesCount = AllFaultyDevices.count()
    AllCriticalDevices = FamilyDeviceReg.objects.filter(Q(user = request.user) & Q(devicestatus = 'Critical'))
    AllCriticalDevicesCount = AllCriticalDevices.count()
    AllFaultyAndCritialDevices = AllFaultyDevicesCount + AllCriticalDevicesCount
    AllWorkingDevices = FamilyDeviceReg.objects.filter(Q(user = request.user) & Q(devicestatus = 'Working'))
    AllWorkingDevicesCount = AllWorkingDevices.count()

    
    context = {'allfamilymembers':allfamilymembers, 'AllFamilyDevices':AllFamilyDevices, 'AllFamilyDevicesCount':AllFamilyDevicesCount, 'AllWorkingDevicesCount':AllWorkingDevicesCount, 'AllFaultyAndCritialDevices':AllFaultyAndCritialDevices}
    return render(request, 'familydhmsapp/familyinventory.html', context)


@login_required(login_url='UserLogin')
def FamilyDeviceMaintenance(request):
    AllFamilyMaintainanceReq = FamilyMaintainanceReq.objects.filter(user=request.user)
    context = {'AllFamilyMaintainanceReq':AllFamilyMaintainanceReq}
    return render(request, 'familydhmsapp/familymaintain.html', context)


@login_required(login_url='UserLogin')
def FamilyAnalytics(request):
    return render(request, 'familydhmsapp/familyanalytics.html')


@login_required(login_url='UserLogin')
def FamilySupport(request):
    return render(request, 'familydhmsapp/familysupport.html')


@login_required(login_url='UserLogin')
def FamilySettings(request):
    return render(request, 'familydhmsapp/familysettings.html')

@login_required(login_url='UserLogin')
def FamilyMembers(request):
    if request.method == 'POST' and 'email' in request.POST:
        fullname = request.POST['fullname']
        email = request.POST['email']
        memberphone = request.POST['memberphone']
        memberid = 'FM-'  + get_random_string(length=5)

        if not request.POST['fullname']:
            messages.error(request, 'Registration Failed: Kindly provide a full name for this family member.')
            return redirect('FamilyMembers')

        if not request.POST['email']:
            messages.error(request, 'Registration Failed: Kindly provide an email address for this family member.')
            return redirect('FamilyMembers')

        if not request.POST['memberphone']:
            messages.error(request, 'Registration Failed: Kindly provide an phone number for this family member.')
            return redirect('FamilyMembers')

        checkemail = User.objects.filter(email = request.POST['email'])
        checkfullname = User.objects.filter(first_name = request.POST['fullname'])
        checkfamilyemail = FamilyMemberReg.objects.filter(memberemail = request.POST['email'])
        checkfamilyfullname = FamilyMemberReg.objects.filter(memberfullname = request.POST['fullname'])
        checkfamilyPhoneNumber = FamilyMemberReg.objects.filter(memberphone = request.POST['memberphone'])
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

        if (checkfamilyPhoneNumber):
            messages.error(request, 'Registration Failed: Phone Number is already registered to an existing user.')
            return redirect('FamilyMembers')

        familymemberform = FamilyMemberReg(user = request.user, memberfullname = fullname, memberemail = email, memberid = memberid, memberphone = memberphone, familyid = request.user.last_name)

        try:
            familymemberform.save()
            messages.success(request, "You registered a family member successfully.")
            return redirect('FamilyMembers')
        except:
            messages.error(request, "An error occured while saving family member. Kindly try again.")
            return redirect('FamilyMembers')
    allfamilymembers = FamilyMemberReg.objects.filter(user = request.user)
    allfamilymembersCount = allfamilymembers.count()
    AllFamilyDevices = FamilyDeviceReg.objects.filter(user = request.user)
    context = {'allfamilymembers':allfamilymembers, 'allfamilymembersCount':allfamilymembersCount, 'AllFamilyDevices':AllFamilyDevices}
    return render(request, 'familydhmsapp/familymember.html', context)


def FamilyLogout(request):
    logout(request)
    messages.error(request, 'Logout Successfull.')
    return redirect('UserLogin')


# AUTO COMPLETE SETUP STARTS HERE
# def autocompleteModel(request):
    # if request.is_ajax():
    #     q = request.GET.get('term', '').capitalize()
    #     search_qs = FamilyDeviceReg.objects.filter(name__startswith=q)
    #     results = []
    #     print (q)
    #     for r in search_qs:
    #         results.append(r.deviceid)
    #     data = json.dumps(results)
    # else:
    #     data = 'fail'
    # mimetype = 'application/json'
    # return HttpResponse(data, mimetype)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def autocompleteModel(request):
    # if request.is_ajax():
    if is_ajax(request=request):
        q = request.GET.get('term', '').capitalize()
        search_qs = FamilyDeviceReg.objects.filter(
       Q( Q(deviceid__icontains = q) | 
        Q(devicebrand__icontains = q) |
        Q(deviceOS__icontains = q) |
        Q(devicemodel__icontains = q) |
        Q(deviceyearofpurchase__icontains = q) |
        Q(devicename__icontains = q) |
        Q(devicemacaddress__icontains = q) |
        Q(deviceipaddress__icontains = q) |
        Q(devicetype__icontains = q) |
        Q(deviceUserID__icontains = q) |
        Q(deviceuserfullname__icontains = q) |
        Q(devicestatus__icontains = q)
    ) & Q(user = request.user))

        results = []
        for r in search_qs:
            results.append(r.devicename)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
    

# AUTO COMPLETE SETUP ENDS HERE

# FAMILY DEVICE DETAILS SECTION STARTS HERE
@login_required(login_url='UserLogin')
def FamilyDeviceDetails(request, deviceid):
    curretdevice = FamilyDeviceReg.objects.get(Q(user = request.user) and Q(deviceid = deviceid))
    if request.method == 'POST':
        try:
            uniqueMaintenanceID = 'Maintainance -'  + get_random_string(length=5)
            title = request.POST['title']
            description = request.POST['details']
            FamilyMaintainanceReqForm = FamilyMaintainanceReq(maintaindeviceID = curretdevice.deviceid, user = request.user,
            maintainancetitle = title, maintainancedescription = description, maintainanceID = uniqueMaintenanceID, FamilyUniqueCode = request.user.last_name)
            FamilyMaintainanceReqForm.save()

            messages.success(request, "Maintenance request was created successfully. A support staff will attend to this shortly.")
            return redirect('FamilyDeviceMaintenance')

        except:
            messages.success(request, "An error occured while creating a maintenance reqeust. Kindly try again.")
            return redirect('FamilyDeviceDetails', deviceid)

    context = {'curretdevice' : curretdevice}
    return render(request, 'familydhmsapp/familydevdetails.html', context)


# FAMILY DEVICE DETAILS SECTION ENDS HERE


@login_required(login_url='UserLogin')
def FamilySubAdminFxn(request, pk):
    familymember = FamilyMemberReg.objects.filter(Q(user = request.user) and Q(id = pk))
    # print(familymember.values_list('memberemail', flat=True))
    if familymember:
        Reqfamilyadmin = request.user
        FamilySubAdminForm = FamilySubAdmin(user = Reqfamilyadmin, FamilyUniqueCode = request.user.last_name,  userfullname = familymember.values_list('memberfullname', flat=True), useremail = familymember.values_list('memberemail', flat=True))
        FamilySubAdminForm.save()
        messages.success(request, f'You added a subadmin on your account')
        return redirect('FamilyMembers')
    else:
        messages.error(request, "An error occured. Kindly try again.")
        return redirect('FamilyMembers')
    return render(request, 'familydhmsapp/familymember.html', context)










