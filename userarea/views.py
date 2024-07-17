# from site import USER_BASE
from django.urls import reverse
from django.contrib import messages

from aichat.models import AIChat_Room
from .models import *
from useronboard.models import LoginStatus
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout, authenticate
import csv
from django.db.models import Q
from useronboard.models import SignupForm, UserProfileImage
from datetime import datetime
from datetime import date
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import json
# import winapps
import random
import string
import time
import os

def generate_password(length, count):
    passwords = []
    for i in range(count):
        password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
        passwords.append(password)
    return passwords
    # generate_password(10, 1)

# FIND ALL INSTALLED APPS TRIAL STARTS HERE
# importing the module
import subprocess

# traverse the software list
# Data = subprocess.check_output(['wmic', 'product', 'get', 'name'])
# a = str(Data)
  
# # try block
# try:    
#     # arrange the string
#     for i in range(len(a)):
#         RawListOfApp = a.split("\\r\\r\\n")[6:]
#         RawListOfAppName = RawListOfApp[6:][i]
#         RawListOfAppDetail = RawListOfApp[i]
#         print(RawListOfAppName)
  
# except IndexError as e:
#     print("All Done")
# Create your views here.
# FIND ALL INSTALLED APPS TRIAL ENDS HERE


import platform
# Get the operating system name
os_name = platform.system()

# Print the operating system name
# print("Operating System:", os_name)


@login_required(login_url='Login')
def NavBar(request):
    if request.method == 'POST' and 'startAISession' in request.POST:
        uniqueId = 'AI_Chat-' + get_random_string(length=5)
        createAIChat_Room = AIChat_Room.objects.create(uniqueId = uniqueId, companyID = request.user.last_name)
        createAIChat_Room.save()
        if createAIChat_Room:
            return redirect('AiChatPage')
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    allSignUps = SignupForm.objects.filter(user = request.user)
    context = {'allSignUps': allSignUps, 'AllMaintenanceRequests':AllMaintenanceRequests}
    return render(request, 'general.html', context)




@login_required(login_url='Login')
def Reports(request):
    allUsers = User.objects.all()
    allSignUps = SignupForm.objects.all()
    allDevices = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = request.user.last_name)
    allDevicesCount = allDevices.count()
    allDevicesMonthPre = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = request.user.last_name)
    allDevicesMonth = allDevicesMonthPre.values_list('registeredMonth')
    JanDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Jan'))
    JanDevices1 = JanDevices.count()
    FebDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Feb'))
    FebDevices1 = FebDevices.count()
    MarDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Mar'))
    MarDevices1 = MarDevices.count()
    AprDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Apr'))
    AprDevices1 = AprDevices.count()
    MayDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'May'))
    MayDevices1 = MayDevices.count()
    JuneDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Jun'))
    JuneDevices1 = JuneDevices.count()
    JulyDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Jul'))
    JulyDevices1 = JulyDevices.count()
    AugDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Aug'))
    AugDevices1 = AugDevices.count()
    SeptDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Sep'))
    SeptDevices1 = SeptDevices.count()
    OctDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Oct'))
    OctDevices1 = OctDevices.count()
    NovDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Nov'))
    NovDevices1 = NovDevices.count()
    DecDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(registeredMonth = 'Dec'))
    DecDevices1 = DecDevices.count()

    # Amounts = ['100,000', '200,000', '300,000', '400,000', '500,000']

    data = [JanDevices1, FebDevices1, MarDevices1, AprDevices1, MayDevices1, JuneDevices1, JulyDevices1, AugDevices1, SeptDevices1, OctDevices1, NovDevices1, DecDevices1]
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    AllMaintenances = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name).count()
    # AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)

    context = {'AllMaintenanceRequests':AllMaintenanceRequests, 'JanDevices':JanDevices, 'FebDevices':FebDevices, 'AugDevices':AugDevices, 'SeptDevices':SeptDevices, 
    'OctDevices':OctDevices, 'NovDevices':NovDevices, 'DecDevices':DecDevices, 'MarDevices':MarDevices, 
    'AprDevices':AprDevices, 'MayDevices':MayDevices,'JuneDevices':JuneDevices, 'JulyDevices':JulyDevices, 
    'labels':labels, 'data':data, 'allDevicesMonth':allDevicesMonth, 'allDevices':allDevices, 
    'allSignUps':allSignUps, 'allUsers':allUsers, 'AllMaintenances':AllMaintenances, 'allDevicesCount':allDevicesCount}

    return render(request, 'userarea/reports.html', context)


@login_required(login_url='Login')
def Support(request):
    allProfileImages = UserProfileImage.objects.all().first
    allUsers = User.objects.all()
    allSignUps = SignupForm.objects.all()
    if request.method == 'POST' and 'startAISession' in request.POST:
        print('clicked nowww')
        uniqueId = 'AI_Chat-' + get_random_string(length=5)
        createAIChat_Room = AIChat_Room.objects.create(uniqueId = uniqueId, companyID = request.user.last_name)
        createAIChat_Room.save()
        if createAIChat_Room:
            return redirect('AiChatPage')
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'AllMaintenanceRequests':AllMaintenanceRequests, 'allSignUps':allSignUps, 'allUsers':allUsers, 'allProfileImages':allProfileImages}
    return render(request, 'userarea/support.html', context)



@login_required(login_url='Login')
def Maintainance(request):
    if request.method == 'GET' and 'dataToExport'  in request.GET:
        dataToExport = request.GET.get('dataToExport') if request.GET.get('dataToExport') != None else ''
        dataToExportNew = list(dataToExport.split(","))
        dataToExportNewNoDuplicate = []
        [dataToExportNewNoDuplicate.append(i) for i in dataToExportNew if i not in dataToExportNewNoDuplicate]
        # get latest array entry ID for edit and delete features
        maintainElementID = dataToExportNewNoDuplicate[-1]
        maintainElementIDMain = MaintenanceRequest.objects.get(MaintainRequestID = maintainElementID).pk
        for i in dataToExportNew:
            if dataToExportNew.count(i) == 2:
                dataToExportNew.remove(i)

            response = HttpResponse(content_type = 'text/csv')
            writer = csv.writer(response)
            writer.writerow(['Device Name', 'Device ID', 'Device IP Address', 'Device MAC ID', 
            'Device Type', 'Device Category', 'Device Location', 'Maintenance Status', 'Device User', 
            'Maintenance Requester', 'Maintenance Request ID', 'Maintenance Request Description', 'Date For Request'])

            # for data in dataToExportNewNoDuplicate:
            for data in dataToExportNew:
                if data is not None:
                    for maintenanceDevice in MaintenanceRequest.objects.filter(MaintainRequestID = data).values_list('MaintainDeviceName', 
                    'MaintainDeviceID', 'MaintainDeviceIP', 'MaintainDeviceMAC_ID', 'MaintainType', 'MaintainDeviceCategory', 
                    'MaintainDeviceLocation', 'MaintainStatus', 'MaintainDeviceUserFirstname', 'MaintainRequestID', 
                    'MaintainRequestDescription', 'created_at'):
                        writer.writerow(maintenanceDevice)

                    response['Content-Disposition'] = 'attachment; filename =  maintenancerequests.csv'
                    messages.error(request, 'Export complete.')
                else:
                    messages.error(request, 'Please select a section to export.')
                    return redirect('Maintainance')

            return response
    
    if request.method == 'GET' and 'deviceToDelete' in request.GET:
        currentDevice = MaintenanceRequest.objects.all()
        deviceToDelete = request.GET['deviceToDelete']
        deviceToDeleteArr = []
        deviceToDeleteArrNew = []
        deviceToDeleteArr = list(deviceToDelete.split(","))
        for i in deviceToDeleteArr:
            if len(deviceToDeleteArr) == 1:
                currentDevice = MaintenanceRequest.objects.get(MaintainRequestID = i)
                messages.error(request, 'Maintenance Request(s) deleted succesfully.')
                currentDevice.delete()
                # return redirect('Maintainance')
            else:
                print(i)
                currentDevice = MaintenanceRequest.objects.get(MaintainDeviceName = i)
                print(currentDevice)
                currentDevice.delete()
                messages.error(request, 'Maintenance Request(s) deleted succesfully.')
        return redirect('Maintainance')

    # REDIRECT TO VIEW DETAILS PAGE FOR SELECTED MAINTENANCE REQUEST
    if request.method == 'GET' and 'requesttoviewdetails' in request.GET:
        requesttoviewdetailsMain = request.GET['requesttoviewdetails']
        print(' see requesttoviewdetailsMain below:')
        print(requesttoviewdetailsMain)
        currentDevice = MaintenanceRequest.objects.filter(MaintainRequestID = requesttoviewdetailsMain)
        return redirect('MaintainanceDetails', name = requesttoviewdetailsMain )
        # return redirect('ProfilePage', pk=currentUser.id)

    # REDIRECT TO EDIT MAINTENANCE REQUEST BELOW
    if request.method == 'GET' and 'idforeditmain' in request.GET:
        idforedit = request.GET['idforeditmain']
        currentDevice = MaintenanceRequest.objects.get(MaintainRequestID = idforedit).MaintainRequestID
        return redirect('EditMaintenenceRequest', name = currentDevice )


    
    if request.method == 'POST' and 'startAISession' in request.POST:
        print('clicked nowww')
        uniqueId = 'AI_Chat-' + get_random_string(length=5)
        createAIChat_Room = AIChat_Room.objects.create(uniqueId = uniqueId, companyID = request.user.last_name)
        createAIChat_Room.save()
        if createAIChat_Room:
            return redirect('AiChatPage')


    # allMaintainsByStaff = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name or request.user.last_name)
    allMaintainsByStaff = MaintenanceRequest.objects.filter(Q(CompanyUniqueCode = request.user.last_name) or Q(CompanyUniqueCode = request.user.email) )
    allMaintainsCount = allMaintainsByStaff.count()

    # AllMaintainDevice = MaintenanceRequest.objects.get(MaintainRequestID = name)

    numberOfDevicesPerPage = DeviceCountPerPage.objects.filter(user = request.user).first()
    allProfileImages = UserProfileImage.objects.all().first
    allUsers = User.objects.all()
    allSignUps = SignupForm.objects.all()
    allCompletedRequests = MaintenanceRequest.objects.filter(Q(MaintainStatus = 'Completed') & Q(user = request.user))
    allCompletedRequestsCount = allCompletedRequests.count()
    allCanceledRequests = MaintenanceRequest.objects.filter(Q(MaintainStatus = 'Canceled') & Q(user = request.user))
    allCanceledRequestsCount = allCanceledRequests.count()
    allOngoingRequests = MaintenanceRequest.objects.filter(Q(MaintainStatus = 'Ongoing') & Q(user = request.user))
    allOngoingRequestsCount = allOngoingRequests.count()
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'AllMaintenanceRequests':AllMaintenanceRequests, 'allOngoingRequestsCount':allOngoingRequestsCount, 'allCompletedRequestsCount':allCompletedRequestsCount, 'allCanceledRequestsCount':allCanceledRequestsCount, 'allSignUps':allSignUps, 'allUsers':allUsers, 'allProfileImages':allProfileImages, 'allMaintainsByStaff':allMaintainsByStaff, 'allMaintainsCount':allMaintainsCount, 'numberOfDevicesPerPage':numberOfDevicesPerPage}
    return render(request, 'userarea/maintainance.html', context)



@login_required(login_url='Login')
def MaintainanceDetails(request, name):
    if request.method == 'POST' and 'addedComment' in request.POST:
        addedComentMain = request.POST['addedComment']
        if addedComentMain == '':
            return redirect('MaintainanceDetails', name = name)
        commenter = request.POST['commenter']
        commenterEmailAddress= request.POST['commenterEmailAddress']
        CommentedMaintainDeviceName = request.POST['CommentedMaintainDeviceName']
        CommentedMaintainDeviceUser = request.POST['CommentedMaintainDeviceUser']
        CommentedMaintainRequester = request.POST['CommentedMaintainRequester']
        CommentedMaintainRequestID = request.POST['CommentedMaintainRequestID']
        # commenterEmail = request.POST['commenterEmail']
        form = AddedMaintenanceComments.objects.create(
            commenterEmailAddress = commenterEmailAddress,
            commenter = commenter,
            commentProper = addedComentMain,
            CommentedMaintainDeviceName = CommentedMaintainDeviceName,
            CommentedMaintainDeviceUser = CommentedMaintainDeviceUser, 
            CommentedMaintainRequester = CommentedMaintainRequester,
            CommentedMaintainRequestID = CommentedMaintainRequestID,
            # commenterEmail = commenterEmail
        )
        form.save()

    currentDevice = str(MaintenanceRequest.objects.get(MaintainRequestID = name).MaintainRequestID)
    AllCommments = AddedMaintenanceComments.objects.all()

    currentDeviceMain = str(MaintenanceRequest.objects.get(MaintainRequestID = name).MaintainDeviceID)
    print(currentDeviceMain)
    currentDeviceDetails = DeviceRegisterUpload.objects.get(deviceid = currentDeviceMain).staffUserID
    currentDeviceUser = StaffDataSet.objects.get(StaffID = currentDeviceDetails)
    print(currentDeviceUser)
    
    AllMaintainDevice = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'currentDeviceDetails':currentDeviceDetails, 'currentDeviceUser':currentDeviceUser, 'AllMaintenanceRequests':AllMaintenanceRequests, 'AllCommments':AllCommments, 'AllMaintainDevice':AllMaintainDevice, 'currentDevice':currentDevice}
    return render(request, 'userarea/maintainrequestdetails.html', context)



def DeleteAddedComment(request, pk, name):
    commentToDelete = AddedMaintenanceComments.objects.get(id = pk)
    commentToDelete.delete()
    messages.error(request, 'Comment has been deleted')
    # return response
    return redirect('MaintainanceDetails', name = name)


def EditMaintenenceRequest(request, name):
    selectedRequest = MaintenanceRequest.objects.get(MaintainRequestID = name)
    # selectedRequest = MaintenanceRequest.objects.get(MaintainDeviceName = name)
    form = EditMaintenanceRequest(request.POST or None, instance = selectedRequest)
    if request.POST and form.is_valid():
        print('data validated!')
        form.save()
        return redirect('MaintainanceDetails', name = name)
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'AllMaintenanceRequests':AllMaintenanceRequests, 'form':form, 'selectedRequest':selectedRequest}
    return render(request, 'userarea/editmaintenancereq.html', context)


def AllMaintenanceDelete(request):
    AllRequests = MaintenanceRequest.objects.filter(user = request.user)
    messages.error(request, 'All maintenance request have been deleted successfully!')
    AllRequests.delete()
    return redirect('Maintainance')


def ExportMaintenance(request):
        response = HttpResponse(content_type = 'text/csv')
        writer = csv.writer(response)
        writer.writerow(['Device Name', 'Device ID', 'Device IP Address', 'Device MAC ID', 
        'Device Type', 'Device Category', 'Device Location', 'Maintenance Status', 'Device User', 
        'Maintenance Requester', 'Maintenance Request ID', 'Maintenance Request Description', 'Date For Request'])
        for maintenanceDevice in MaintenanceRequest.objects.filter(user = request.user).values_list('MaintainDeviceName', 
        'MaintainDeviceID', 'MaintainDeviceIP', 'MaintainDeviceMAC_ID', 'MaintainType', 'MaintainDeviceCategory', 
        'MaintainDeviceLocation', 'MaintainStatus', 'MaintainDeviceUser', 'MaintainRequester', 'MaintainRequestID', 
        'MaintainRequestDescription', 'created_at'):
            writer.writerow(maintenanceDevice)
        response['Content-Disposition'] = 'attachment; filename =  maintenancerequests.csv'

        return response

        return render(request, 'userarea/maintainance.html')


@login_required(login_url='Login')
def Settings(request):
    allProfileImages = UserProfileImage.objects.all().first
    allUsers = User.objects.all()
    allSignUps = SignupForm.objects.all()
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'AllMaintenanceRequests':AllMaintenanceRequests, 'allSignUps':allSignUps, 'allUsers':allUsers, 'allProfileImages':allProfileImages}
    return render(request, 'userarea/settings.html', context)



# findDeviceInventoryhere
@login_required(login_url='Login')
def DeviceInventory(request):
    today = date.today()
    dateForWeekNumber = datetime.today()
    weekNumber = dateForWeekNumber.isocalendar().week
    if request.method == 'POST' and 'deviceusedepartment' in request.POST:
        uniqueId = 'Device-' + get_random_string(length=5)
        if request.POST['devicebrand']:
            randomNumber = random.randint(100, 9999)
            DeviceBrandProper = request.POST['devicebrand']+ '_' + str(randomNumber)
        else: 
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Brand.")
            return redirect('DeviceInventory')

        if request.POST['deviceyearofpurchase']:
            depreciateRate = 2024 - int(request.POST['deviceyearofpurchase'])
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
            return redirect('DeviceInventory')

            
        deviceusedepartment = request.POST['deviceusedepartment']
        devicetype = request.POST['devicetype']
        devicebrand = request.POST['devicebrand']
        deviceos = request.POST['deviceos']
        devicecostofpurchase = request.POST['devicecostofpurchase']
        deviceyearofpurchase = request.POST['deviceyearofpurchase']
        devicename = request.POST['devicename']
        devicemacaddress = request.POST['devicemacaddress']
        devicelocation = request.POST['devicelocation']
        deviceip = request.POST['deviceip']
        devicestatus = request.POST['devicestatus']
        staffUserID = request.POST['staffUserID']
        CompanyUniqueCode = request.user.last_name
        # CompanyUniqueCode = request.POST['CompanyUniqueCode']
        user = request.user
        StaffUniqueId = 'Staff-' + username + str(generate_password(10, 1))

        if not request.POST['deviceusedepartment']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Department.")
            return redirect('DeviceInventory')
        
        # if not request.POST['devicebrand']:
        #     messages.error(request, "Device uploaded failed. Please Indicate This Device's Brand.")
        #     return redirect('DeviceInventory')
        
        if not request.POST['devicemacaddress']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's MAC Address.")
            return redirect('DeviceInventory')
        
        if not request.POST['devicetype']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Type.")
            return redirect('DeviceInventory')
        
        
        if (DeviceRegisterUpload.objects.filter(Q(Q(devicename = request.POST['devicename']) & Q(user = request.user)))):
            messages.success(request, f'Upload Failed: the device: {devicename} already exists in your system. Please change the device name and try again')
            return redirect('DeviceInventory')

        # if not request.POST['deviceyearofpurchase']:
            

        if not request.POST['devicelocation']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Location.")
            return redirect('DeviceInventory')
        
        if not request.POST['devicestatus']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Working Condition.")
            return redirect('DeviceInventory')
        
        SaveDeviceProper = DeviceRegisterUpload.objects.create(
            deviceusedepartment=deviceusedepartment, devicetype=devicetype, devicebrand=DeviceBrandProper, 
            deviceos=deviceos, devicecostofpurchase=devicecostofpurchase, devicename=devicename,
            devicemacaddress=devicemacaddress, devicelocation=devicelocation, deviceip=deviceip,
            devicestatus=devicestatus, staffUserID=StaffUniqueId, CompanyUniqueCode=CompanyUniqueCode,
            deviceyearofpurchase=deviceyearofpurchase, user=user, devicedepreciationrate=depreciateRateReal,
            deviceid=uniqueId
        )

        # SAVE FAULTY OR CRITICAL DEVICES 
        if request.POST['devicestatus'] == 'Faulty' or request.POST['devicestatus'] == 'Critical':
            CompanyFaultyDevicesForm = CompanyFaultyDevices(user = request.user, deviceID = uniqueId, month = today.strftime("%b"), year = today.strftime("%B %d, %Y"), CompanyUniqueCode = request.user.last_name)
            CompanyFaultyDevicesForm.save()  
        

        try:
            SaveDeviceProper.save()
            messages.success(request, 'Device uploaded successfully')
            return redirect('DeviceInventory')
        except:
            messages.error(request, 'Device uploaded failed. Please Try again.')
            return redirect('DeviceInventory')


    # CSV UPLOAD STARTS HERE
    if request.method == "POST" and 'csv_file' in request.FILES:
        print('file uploaded')
        username = request.POST['username']
        filedata = request.FILES.get('csv_file', False)
        
        if 'csv' not in str(filedata):
            messages.success(request, 'Wrong File Format. Please Use The Recommended CSV File.')
            return redirect('DeviceInventory')

        if request.FILES.get('csv_file') is None:
            messages.success(request, 'Device List Updated Failed! Please Select A File.')
            return redirect('DeviceInventory')
        
        if not request.POST['username']:
            messages.success(request, 'Device List Updated Failed! User Name Missing Login Again.')
            return redirect('DeviceInventory')
        

        form = uploadedDeviceData.objects.create(user = request.user, username = username, mainfile = filedata)
        obj = uploadedDeviceData.objects.filter(user = request.user).first()
        print('file saved')

        with open(obj.mainfile.path, 'r') as f:
            print('file opened')
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                randomNumberForStaff = random.randint(1000, 9999999)
                StaffUniqueId = 'Staff-' + request.user.username + str(randomNumberForStaff)
                print('file reder starter')
                if i == 0:
                    pass
                elif (DeviceRegisterUpload.objects.filter(Q(Q(devicename = row[1]) & Q(user = request.user)))):
                    messages.success(request, f'Upload Failed: the device: {row[1]} already exists in your system. Please change the device name and try again')
                    return redirect('DeviceInventory')
                elif len(row) < 21:
                    messages.success(request, 'Upload Failed: Please Use The Sample CSV File Provided')
                    return redirect('DeviceInventory')
                elif len(row) > 21:
                    today = date.today()
                    dateForWeekNumber = datetime.today()
                    randomNumber = random.randint(100, 99999)
                    weekNumber = dateForWeekNumber.isocalendar().week
                    randomNumberForStaff = random.randint(1000, 99999)
                    uniqueId = 'Device-' + get_random_string(length=5)
                    if row[21]:
                        depreciateRate = 2023 - int(row[21])
                    else:
                        depreciateRate = 2020
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
                    
                    if (row[17] == ''):
                        row[17] = f'{request.user}_Staff_{StaffUniqueId}'
                    elif ('@' not in row[17]):
                        row[17] = f'{request.user}_Staff_{StaffUniqueId}'
                    else:
                        row[17] = row[17]               
                    if (StaffDataSet.objects.filter(Q(Q(staff_email = row[17]) & Q(user = request.user)))):
                        ExisitingStaffID = StaffDataSet.objects.filter(Q(Q(staff_email = row[17]) & Q(user = request.user))).first().StaffID
                        StaffUniqueId = ExisitingStaffID
                    else:
                        StaffUniqueId = StaffUniqueId
                        StaffDataSet.objects.create(
                            user = request.user,
                            StaffID = StaffUniqueId,
                            staff_firstname = row[4],
                            staff_lastname = row[5],
                            staff_phonenumber = row[18],
                            staff_location = row[13],
                            staff_email = row[17],
                            staff_role = row[8],
                            CompanyUniqueCode = request.user.last_name
                            ),
                        User.objects.create_user(
                            username = row[17], email = StaffUniqueId, password =  StaffUniqueId, first_name = request.user.last_name, last_name = row[4] +' '+row[5]
                            )

                    DeviceRegisterUpload.objects.create(
                        user = request.user,
                        deviceip = row[0],
                        devicename = row[1],
                        devicemacaddress = row[2],
                        devicenetworkadaptercompany = row[3],
                        devicestatus = row[6],
                        deviceworkgroup = row[7],
                        deviceusedepartment = row[8],
                        deviceportnumber = row[9],
                        devicemultiplepacket = row[10],
                        index = row[11],
                        devicetype = row[12],
                        devicelocation = row[13],
                        devicebrand = row[14],
                        deviceos = row[15],
                        devicecostofpurchase = row[16],
                        deviceuserphonenumber = row[18],
                        deviceuserdateofresumption = row[19],
                        deviceworkingcondition = row[20],
                        deviceyearofpurchase = row[21],
                        devicedepreciationrate = depreciateRateReal,
                        deviceid = uniqueId,
                        staffUserID = StaffUniqueId,
                        savetimedata = today.strftime("%B %d, %Y"),
                        registeredMonth = today.strftime("%b"),
                        weekNumberSaved = weekNumber,
                        CompanyUniqueCode = request.user.last_name
                    )
                    
                    
                    # SAVE FAULTY OR CRITICAL DEVICES 
                    if row[6] == 'Faulty' or row[6] == 'Critical' or row[6] == 'Bad':
                        CompanyFaultyDevicesForm = CompanyFaultyDevices(user = request.user, deviceID = uniqueId, month = today.strftime("%b"), year = today.strftime("%B %d, %Y"), CompanyUniqueCode = request.user.last_name)
                        CompanyFaultyDevicesForm.save() 

                else:
                    messages.error(request, 'Device List Updated Unsuccessfully: Please Fill CSV File And Upload Again')
                    return redirect('DeviceInventory')
            obj.save()
        messages.success(request, 'Device List Updated Successfully')
        return redirect('DeviceInventory')
                    
    # CSV UPLOAD ENDS HERE

    # PAGINATION COUNT FORM STARTS HERE
    if request.method == 'POST'  and 'numofitemsperpage' in request.POST:
        count = str(request.POST['numofitemsperpage'])
        form = DeviceCountPerPage(user = request.user, count = count)
        form.save()
        messages.success(request, 'Device display per page count saved successfully')
        return redirect('DeviceInventory')
    # PAGINATION COUNT FORM ENDS HERE

    
    # GROUP AND DELETE FUNCTIONALY STARTS HERE
    if request.method == 'GET' and 'deviceToDelete' in request.GET:
        currentDevice = DeviceRegisterUpload.objects.all()
        deviceToDelete = request.GET['deviceToDelete']
        deviceToDeleteArr = []
        deviceToDeleteArrNew = []
        deviceToDeleteArr = list(deviceToDelete.split(","))
        print(len(deviceToDeleteArr))
        for i in deviceToDeleteArr:
            if len(deviceToDeleteArr) == 1:
                currentDevice = DeviceRegisterUpload.objects.get(deviceid = i)
                messages.error(request, 'Device(s) deleted succesfully.')
                currentDevice.delete()
                # return redirect('DeviceInventory')
            else:
                print(i)
                currentDevice = DeviceRegisterUpload.objects.get(deviceid = i)
                print(currentDevice)
                currentDevice.delete()
                messages.error(request, 'Device(s) deleted succesfully.')
        return redirect('DeviceInventory')

        # GROUP AND DELETE FUNCTIONALY ENDS HERE

    # EXPORT DEVICE DATA SETTINGS STARTS HERE 
    if request.method == 'GET' and 'dataToExport'  in request.GET:
        dataToExport = request.GET.get('dataToExport') if request.GET.get('dataToExport') != None else ''
        dataToExportNew = list(dataToExport.split(","))
        # print(type(dataToExportNew))
        dataToExportNewNoDuplicate = []
        [dataToExportNewNoDuplicate.append(i) for i in dataToExportNew if i not in dataToExportNewNoDuplicate]
        # get latest array entry ID for edit and delete features
        maintainElementID = dataToExportNewNoDuplicate[-1]
        maintainElementIDMain = DeviceRegisterUpload.objects.get(deviceid = maintainElementID)
        print(maintainElementIDMain)
        for i in dataToExportNew:
            if dataToExportNew.count(i) == 2:
                dataToExportNew.remove(i)
            # print(dataToExportNewNoDuplicate.count(i))

            response = HttpResponse(content_type = 'text/csv')
            writer = csv.writer(response)
            writer.writerow(['Device IP', 'Device Name', 'Device MAC Address', 'Device Network Adapter Company', 'Device User Firstname', 'Device User Lastname',
            'Device Status', 'Device Workgroup', 'Device Department', 'Device Port Number', 'Device Multiple Packet', 'Device Type', 'Device Location', 'Device Brand', 
            'Device OS', 'Device Cost Of Purchase', 'Device User Email Address', 'Device User Phone Number', 'Device User Date Of Job Resumption', 'Device Working Condition', 'Device Year Of Purchase', 'Device Depreciation Rate', 'Device ID'])

            # for data in dataToExportNewNoDuplicate:
            for data in dataToExportNew:
                if data is not None:
                    for DeviceInfo in DeviceRegisterUpload.objects.filter(deviceid = data).values_list('deviceip', 'devicename', 'devicemacaddress',
                    'devicenetworkadaptercompany', 'deviceuserfirstname', 'deviceuserlastname', 'devicestatus', 'deviceworkgroup', 'deviceusedepartment', 'deviceportnumber', 'devicemultiplepacket', 'devicetype', 
                    'devicelocation', 'devicebrand', 'deviceos', 'devicecostofpurchase', 'deviceuseremail', 'deviceuserphonenumber', 'deviceuserdateofresumption', 'deviceworkingcondition', 'deviceyearofpurchase', 'devicedepreciationrate',
                    'deviceid'):
                        writer.writerow(DeviceInfo)

                    response['Content-Disposition'] = 'attachment; filename =  DeviceRegisterUploads.csv'
                    messages.error(request, 'Export complete.')
                else:
                    messages.error(request, 'Please select a section to export.')
                    return redirect('DeviceInventory')

            return response
            # EXPORT DEVICE DATA DETAILS ENDS HERE

     # REDIRECT TO EDIT Details REQUEST BELOW
    if request.method == 'GET' and 'idforeditmain' in request.GET:
        idforedit = request.GET['idforeditmain']
        currentDevice = DeviceRegisterUpload.objects.get(devicebrand = idforedit).deviceid
        return redirect('EditDevice', deviceid = currentDevice )


    # REDIRECT TO VIEW DETAILS VIEW
    if request.method == 'GET' and 'viewdetailsdetails' in request.GET:
        viewdetailsdetailsMain = request.GET['viewdetailsdetails']
        print('see viewdetailsdetailsMain below')
        return redirect('ViewDeviceDetails', name = viewdetailsdetailsMain )
    
    # SAVE DEVICE FROM FORM
    if request.method == 'POST' and 'deviceyearofpurchase' in request.POST:
        return redirect('SaveDevice')


    
    if request.method == 'POST' and 'startAISession' in request.POST:
        print('clicked nowww')
        uniqueId = 'AI_Chat-' + get_random_string(length=5)
        createAIChat_Room = AIChat_Room.objects.create(uniqueId = uniqueId, companyID = request.user.last_name)
        createAIChat_Room.save()
        if createAIChat_Room:
            return redirect('AiChatPage')
        
    # allUploadedDevices = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = request.user.last_name)
    allUploadedDevices = DeviceRegisterUpload.objects.filter(user = request.user)
    AllStaffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.last_name)
    # AllStaffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.last_name)
    workingSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(user = request.user))
    workingSystems2 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Good') & Q(user = request.user))
    workingSystems = workingSystems1.count() + workingSystems2.count()
    badSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Faulty') & Q(user = request.user))
    badSystems = badSystems1.count()
    allUploadedDevicesCount = allUploadedDevices.count()
    numberOfDevicesPerPage = str(DeviceCountPerPage.objects.filter(user = request.user).first())
    allProfileImages = UserProfileImage.objects.all().first
    allSignUps = SignupForm.objects.all()
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'AllMaintenanceRequests':AllMaintenanceRequests, 'AllStaffMembers':AllStaffMembers, 'allSignUps':allSignUps, 'allProfileImages':allProfileImages, 'allUploadedDevices':allUploadedDevices, 'numberOfDevicesPerPage':numberOfDevicesPerPage, 'allUploadedDevicesCount':allUploadedDevicesCount, 'workingSystems':workingSystems, 'badSystems':badSystems}
    return render(request, 'userarea/deviceinventory.html', context)


# SAVE DEVICE ONTO DATA BASE FROM FORM FUNTIONALITY STARTS HERE
def SaveDevice(request):
    deviceusedepartment = request.POST['deviceusedepartment']
    devicetype = request.POST['devicetype']
    devicebrand = request.POST['devicebrand']
    deviceos = request.POST['deviceos']
    devicecostofpurchase = request.POST['devicecostofpurchase']
    deviceyearofpurchase = request.POST['deviceyearofpurchase']
    devicename = request.POST['devicename']
    devicemacaddress = request.POST['devicemacaddress']
    devicelocation = request.POST['devicelocation']
    deviceip = request.POST['deviceip']
    devicestatus = request.POST['devicestatus']
    staffUserID = request.POST['staffUserID']

    if not request.POST['deviceusedepartment']:
        messages.error(request, "Device uploaded failed. Please Indicate This Device's Department.")
        return redirect('DeviceInventory')
    
    if not request.POST['devicebrand']:
        messages.error(request, "Device uploaded failed. Please Indicate This Device's Brand.")
        return redirect('DeviceInventory')
    
    if not request.POST['devicemacaddress']:
        messages.error(request, "Device uploaded failed. Please Indicate This Device's MAC Address.")
        return redirect('DeviceInventory')
    
    if not request.POST['devicetype']:
        messages.error(request, "Device uploaded failed. Please Indicate This Device's Type.")
        return redirect('DeviceInventory')

    if not request.POST['deviceyearofpurchase']:
        messages.error(request, "Device uploaded failed. Please Indicate This Device's Year Of Purchase.")
        return redirect('DeviceInventory')

    if not request.POST['devicelocation']:
        messages.error(request, "Device uploaded failed. Please Indicate This Device's Location.")
        return redirect('DeviceInventory')
    
    if not request.POST['devicestatus']:
        messages.error(request, "Device uploaded failed. Please Indicate This Device's Working Condition.")
        return redirect('DeviceInventory')
    
    SaveDeviceProper = DeviceRegisterUpload.objects.create(
        deviceusedepartment=deviceusedepartment, devicetype=devicetype, devicebrand=devicebrand, 
        deviceos=deviceos, devicecostofpurchase=devicecostofpurchase, devicename=devicename,
        devicemacaddress=devicemacaddress, devicelocation=devicelocation, deviceip=deviceip,
        devicestatus=devicestatus, staffUserID=staffUserID
    )

    try:
        SaveDeviceProper.save()
        messages.success(request, 'Device uploaded successfully')
        return redirect('DeviceInventory')
    except:
        messages.error(request, 'Device uploaded failed. Please Try again.')
        return redirect('DeviceInventory')


    return render(request, 'userarea/deviceinventory.html')

# VIEW DEVICE DETAILS PAGE
def ViewDeviceDetails(request, name):
    randomNumber = random.randint(10, 9999)
    today = date.today()
    if request.method == 'POST' and 'MaintainStatus' in request.POST:
        MaintainStatus = request.POST['MaintainStatus']
        MaintainPriorityStatus = request.POST['MaintainPriorityStatus']
        MaintainDeviceType = request.POST['MaintainDeviceType']
        MaintainType = request.POST['MaintainType']
        MaintainRequestDescription = request.POST['MaintainRequestDescription']
        MaintainDeviceName = request.POST['MaintainDeviceName']
        MaintainDeviceID = request.POST['MaintainDeviceID']
        MaintainDeviceIP = request.POST['MaintainDeviceIP']
        MaintainDeviceMAC = request.POST['MaintainDeviceMAC']
        MaintainDeviceCategory = request.POST['MaintainDeviceCategory']
        MaintainDeviceLocation = request.POST['MaintainDeviceLocation']
        MaintainDeviceUserID = request.POST['MaintainDeviceUserID']
        # MaintainDeviceUserLastname = request.POST['MaintainDeviceUserLastname']
        MaintainRequesterEmailAddress = request.POST['MaintainRequesterEmailAddress']
        MaintainDeviceUserDepartment = request.POST['MaintainDeviceUserDepartment']
        MaintainRequester = request.POST['MaintainRequester']
        CompanyUniqueCode = request.user.last_name
        # currentMonth = request.POST['currentMonthName']
        MaintainRequestID = 'maintain' + '_' + str(randomNumber)

        dateNow = datetime.now()
        month1 = dateNow.strftime("%b")
        print("Current Month Full Name:", month1)
        print("dateNow", dateNow)

        if not request.POST['MaintainStatus']:
            messages.error(request, 'Kindly provide a maintenance status.')
            return redirect('ViewDeviceDetails', name=name)
        
        if not request.POST['MaintainType']:
            messages.success(request, 'Kindly provide a maintenance type.')
            return redirect('ViewDeviceDetails', name=name)
        
        if not request.POST['MaintainRequestDescription']:
            messages.success(request, 'Kindly provide a maintenance description.')
            return redirect('ViewDeviceDetails', name=name)
        

        # check if any request is already filed for this device
        

        form = MaintenanceRequest.objects.create(user = request.user, CompanyUniqueCode = request.user.last_name, MaintainRequesterEmailAddress = MaintainRequesterEmailAddress, MaintainDeviceName = MaintainDeviceName, MaintainDeviceID = MaintainDeviceID, 
        MaintainDeviceIP = MaintainDeviceIP, MaintainType = MaintainType, MaintainDeviceMAC_ID = MaintainDeviceMAC, MaintainDeviceType = MaintainDeviceType, MaintainDeviceUserID = MaintainDeviceUserID,
        MaintainDeviceCategory = MaintainDeviceCategory, MaintainDeviceLocation = MaintainDeviceLocation, MaintainStatus = MaintainStatus, MaintainPriorityStatus=MaintainPriorityStatus,
        currentMonth = month1, MaintainRequester = MaintainRequester, MaintainDeviceUserDepartment = MaintainDeviceUserDepartment, MaintainRequestID = MaintainRequestID, MaintainRequestDescription = MaintainRequestDescription)
        form.save()
        
        # SAVE FAULTY OR CRITICAL DEVICES 
        CompanyFaultyDevicesForm = CompanyFaultyDevices(user = request.user, deviceID = MaintainDeviceID, month = today.strftime("%b"), year = today.strftime("%B %d, %Y"), CompanyUniqueCode = CompanyUniqueCode)
        CompanyFaultyDevicesForm.save()

        # myCompanyEmailAddress = User.objects.filter(last_name = CompanyUniqueCode).values_list('email', flat=True).first()
        # myCompanyName = User.objects.filter(last_name = CompanyUniqueCode).values_list('username', flat=True).first()
        # maintenenceRequestNotification(request, myCompanyEmailAddress, myCompanyName, MaintainRequester, MaintainPriorityStatus, MaintainDeviceMAC, MaintainType, MaintainRequestDescription)

           

        try:
            # find my company mail address
            myCompanyEmailAddress = User.objects.filter(last_name = CompanyUniqueCode).values_list('email', flat=True).first()
            myCompanyName = User.objects.filter(last_name = CompanyUniqueCode).values_list('username', flat=True).first()
            maintenenceRequestNotification(request, myCompanyEmailAddress, myCompanyName, MaintainRequester, MaintainPriorityStatus, MaintainDeviceMAC, MaintainType, MaintainRequestDescription)
        except: 
            print(request, "An error occured while trying to send maintenance notification")
        
        messages.success(request, 'Maintenance request was placed successfully.')
        return redirect('Maintainance')
    
    
    if request.method == 'POST' and 'startAISession' in request.POST:
        # print('clicked nowww')
        uniqueId = 'AI_Chat-' + get_random_string(length=5)
        createAIChat_Room = AIChat_Room.objects.create(uniqueId = uniqueId, companyID = request.user.last_name)
        createAIChat_Room.save()
        if createAIChat_Room:
            return redirect('AiChatPage')
        

    currentDeviceList = DeviceRegisterUpload.objects.get(Q(deviceid = name)  & Q(user = request.user))
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'AllMaintenanceRequests':AllMaintenanceRequests, 'name':name, 'currentDeviceList':currentDeviceList}
    return render(request, 'userarea/devicedetails.html', context)



# EXPORT DEVICES FROM INVENTORY
def ExportDevice(request):
        response = HttpResponse(content_type = 'text/csv')
        writer = csv.writer(response)
        writer.writerow(['Device IP', 'Device Name', 'Device MAC Address', 'Device Network Adapter Company', 'Device User Firstname', 'Device User Lastname',
            'Device Status', 'Device Workgroup', 'Device Department', 'Device Port Number', 'Device Multiple Packet', 'Device Type', 'Device Location', 'Device Brand', 
            'Device OS', 'Device Cost Of Purchase', 'Device User Email Address', 'Device User Phone Number', 'Device User Date Of Job Resumption', 'Device Working Condition', 'Device Year Of Purchase', 'Device Depreciation Rate', 'Device ID'])
        for DeviceInfo in DeviceRegisterUpload.objects.filter(user = request.user).values_list('deviceip', 'devicename', 'devicemacaddress',
                    'devicenetworkadaptercompany', 'deviceuserfirstname', 'deviceuserlastname', 'devicestatus', 'deviceworkgroup', 'deviceusedepartment', 'deviceportnumber', 'devicemultiplepacket', 'devicetype', 
                    'devicelocation', 'devicebrand', 'deviceos', 'devicecostofpurchase', 'deviceuseremail', 'deviceuserphonenumber', 'deviceuserdateofresumption', 'deviceworkingcondition', 'deviceyearofpurchase', 'devicedepreciationrate',
                    'deviceid'):
                        writer.writerow(DeviceInfo)
        response['Content-Disposition'] = 'attachment; filename =  maintenancerequests.csv'

        return response

        return render(request, 'userarea/deviceinventory.html')



# # EDIT DEVICE OPTION ON TABLE ON DEVICE INVENTORY PAGE
# def EditMaintenenceRequest(request, name):
#     selectedRequest = MaintenanceRequest.objects.get(MaintainDeviceName = name)
#     form = EditMaintenanceRequest(request.POST or None, instance = selectedRequest)
#     if request.POST and form.is_valid():
#         print('data validated!')
#         form.save()
#         return redirect('MaintainanceDetails', name = name)
#     context = {'form':form, 'selectedRequest':selectedRequest}
#     return render(request, 'userarea/editmaintenancereq.html', context)



# MAIN DEVICE EDIT DATA PAGE LINKED BELOW
@login_required(login_url='Login')
def EditDevice(request, deviceid):
    MainDeviceData = DeviceRegisterUpload.objects.get(deviceid=deviceid)
    MainDeviceDataStaffUser = DeviceRegisterUpload.objects.filter(deviceid=deviceid).values_list('staffUserID', flat=True).first()
    MainDeviceDataStaffUserFirstName = DeviceRegisterUpload.objects.filter(deviceid=deviceid).values_list('deviceuserfirstname', flat=True).first()
    MainDeviceDataStaffUserLastName = DeviceRegisterUpload.objects.filter(deviceid=deviceid).values_list('deviceuserlastname', flat=True).first()
    
    form = DeviceRegisterForm(request.POST or None, instance = MainDeviceData)
    if request.POST and form.is_valid():
        form.save()
        if form.save():
            messages.success(request, 'Device data saved successfully')
            return redirect('DeviceInventory')
        else:
            messages.success(request, 'Error saving device data')
    AllStaffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'MainDeviceDataStaffUserLastName':MainDeviceDataStaffUserLastName, 'MainDeviceDataStaffUserFirstName':MainDeviceDataStaffUserFirstName, 'MainDeviceDataStaffUser' : MainDeviceDataStaffUser, 'AllStaffMembers':AllStaffMembers, 'form':form, 'id': id, 'MainDeviceData':MainDeviceData}
    return render(request, 'userarea/editdevice.html', context)


@login_required(login_url='Login')
def StaffMembers(request):
    if request.method == 'POST' and 'staff_firstname' in request.POST:
        staff_firstname = request.POST['staff_firstname']
        staff_lastname = request.POST['staff_lastname']
        staff_email = request.POST['staff_email']
        staff_role = request.POST['staff_role']
        staff_phonenumber = request.POST['staff_phonenumber']
        staff_location = request.POST['staff_location']
        CompanyUniqueCode = request.POST['CompanyUniqueCode']
        user = request.user
        username = request.user.username
        randomNumberForStaff = random.randint(1, 99999999)
        # StaffUniqueId = 'Staff-' + request.POST['staff_email'] + str(randomNumberForStaff)
        StaffUniqueId = 'Staff-' + username + str(generate_password(10, 1))
        StaffID = StaffUniqueId

        if not request.POST['staff_phonenumber']:
            messages.error(request, 'Staff registration failed: Please provide a phone number for this staff.')
            return redirect('StaffMembers')
        
        if not request.POST['staff_firstname']:
            messages.error(request, 'Staff registration failed: Please provide a firstname for this staff.')
            return redirect('StaffMembers')
        
        if not request.POST['staff_lastname']:
            messages.error(request, 'Staff registration failed: Please provide a lastname for this staff.')
            return redirect('StaffMembers')

        
        if not request.POST['staff_role']:
            messages.error(request, 'Staff registration failed: Please provide a role for this staff.')
            return redirect('StaffMembers')

        
        if not request.POST['staff_email']:
            messages.error(request, 'Staff registration failed: Please provide an email address for this staff.')
            return redirect('StaffMembers')

        checkUniqueUserMain = User.objects.filter(username = staff_email)
        if checkUniqueUserMain:
            print('checkUniqueUserMain')
            messages.error(request, 'Sorry, a staff with an email address you are trying to upload has already been uploaded.')
            return redirect('StaffMembers')
        else:
            checkUniqueUser =  User.objects.create_user(
            username = staff_email, email = StaffUniqueId, password =  StaffUniqueId, first_name = request.user.last_name, last_name = staff_firstname + ' ' + staff_lastname)

            CreateStaff = StaffDataSet(StaffID=StaffID, staff_firstname=staff_firstname, staff_lastname=staff_lastname, 
            staff_email=staff_email, staff_role=staff_role, staff_phonenumber=staff_phonenumber, user=user,
            staff_location=staff_location, CompanyUniqueCode=CompanyUniqueCode)
            checkUniqueUser.save()
            CreateStaff.save()
            messages.success(request, 'Staff created successfully')
            return redirect('StaffMembers')

    if request.method == 'POST' and 'staffaduploader' in request.POST:
        from datetime import datetime
        # staffADFormMain = StaffADForm(request.POST, request.FILES)
        # if staffADFormMain.is_valid():
        staff_csv_file = request.FILES.get('staff_csv_file', False)
        CompanyUniqueCode = request.user.last_name
        username = request.POST['staffaduploader']

        if not request.FILES.get('staff_csv_file'):
            messages.error(request, 'An error occured. Please review the file and try again')
            return redirect('StaffMembers')

        if not request.POST['CompanyUniqueCode']:
            messages.error(request, 'An error occured.')
            return redirect('StaffMembers')

        if not request.POST['staffaduploader']:
            messages.error(request, 'An error occured. Kindly try again.')
            return redirect('StaffMembers')        
        
        if 'csv' not in str(staff_csv_file):
            messages.error(request, 'You uploaded the wrong File Format. Please use a CSV file instead.')
            return redirect('StaffMembers')
        
        StaffADListForm = StaffADList(staff_csv_file = staff_csv_file, CompanyUniqueCode = request.user.last_name, user = request.user)

        try:
            StaffADListForm.save()
            messages.error(request, 'List uploaded successfully. As soon as setup is complete, this feature will be approved.')
            return redirect('StaffMembers')
        except:
            messages.error(request, 'An error occured. Kindly try again.')
            return redirect('StaffMembers')


    
    if request.method == 'POST' and 'startAISession' in request.POST:
        print('clicked nowww')
        uniqueId = 'AI_Chat-' + get_random_string(length=5)
        createAIChat_Room = AIChat_Room.objects.create(uniqueId = uniqueId, companyID = request.user.last_name)
        createAIChat_Room.save()
        if createAIChat_Room:
            return redirect('AiChatPage')


    staffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.last_name)
    allDevices = DeviceRegisterUpload.objects.all()
    allUploadedDevices = DeviceRegisterUpload.objects.all()
    staffCount = staffMembers.count()
    allSignUps = SignupForm.objects.all()
    AllUsers = User.objects.all()
    AllLoginStatus = LoginStatus.objects.all().first()
    # AllLoginStatus = list(LoginStatus.objects.all().values_list('email', flat=True))
    StaffADListAll = StaffADList.objects.filter(user = request.user).values_list('approvalstatus', flat=True).first()
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'StaffADListAll':StaffADListAll, 'AllLoginStatus':AllLoginStatus, 'AllMaintenanceRequests':AllMaintenanceRequests, 'AllUsers':AllUsers, 'allDevices':allDevices, 'allSignUps':allSignUps, 'staffMembers': staffMembers, 'staffCount':staffCount, 'allUploadedDevices':allUploadedDevices}
    return render(request, 'userarea/staffpage.html', context)


@login_required(login_url='Login')
def StaffDetails(request, id):
    try:
        allStaff = StaffDataSet.objects.get(id = id)
        if request.method == 'POST' and 'deviceusedepartment' in request.POST and 'deviceToAssign' not in request.POST:
            uniqueId = 'Device-' + get_random_string(length=5)
            if request.POST['devicebrand']:
                randomNumber = random.randint(1, 99999)
                DeviceBrandProper = request.POST['devicebrand']+ '_' + str(randomNumber)
            else: 
                messages.error(request, "Device uploaded failed. Please Indicate This Device's Brand.")
                return redirect('DeviceInventory')
    
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
                return redirect('DeviceInventory')
                
            deviceusedepartment = request.POST['deviceusedepartment']
            devicetype = request.POST['devicetype']
            devicebrand = request.POST['devicebrand']
            deviceos = request.POST['deviceos']
            devicecostofpurchase = request.POST['devicecostofpurchase']
            deviceyearofpurchase = request.POST['deviceyearofpurchase']
            devicename = request.POST['devicename']
            devicemacaddress = request.POST['devicemacaddress']
            devicelocation = request.POST['devicelocation']
            deviceip = request.POST['deviceip']
            devicestatus = request.POST['devicestatus']
            staffUserID = allStaff.staffID
            CompanyUniqueCode = request.user.last_name
            user = request.user
    
            if not request.POST['deviceusedepartment']:
                messages.error(request, "Device uploaded failed. Please Indicate This Device's Department.")
                return redirect('DeviceInventory')
            
            
            if (DeviceRegisterUpload.objects.filter(Q(Q(devicename = request.POST['devicename']) & Q(user = request.user)))):
                messages.success(request, f'Upload Failed: the device: {devicename} already exists in your system. Please change the device name and try again')
                return redirect('DeviceInventory')
            
            # if not request.POST['devicebrand']:
            #     messages.error(request, "Device uploaded failed. Please Indicate This Device's Brand.")
            #     return redirect('DeviceInventory')
            
            if not request.POST['devicemacaddress']:
                messages.error(request, "Device uploaded failed. Please Indicate This Device's MAC Address.")
                return redirect('DeviceInventory')
            
            if not request.POST['devicetype']:
                messages.error(request, "Device uploaded failed. Please Indicate This Device's Type.")
                return redirect('DeviceInventory')            
    
            if not request.POST['devicelocation']:
                messages.error(request, "Device uploaded failed. Please Indicate This Device's Location.")
                return redirect('DeviceInventory')
            
            if not request.POST['devicestatus']:
                messages.error(request, "Device uploaded failed. Please Indicate This Device's Working Condition.")
                return redirect('DeviceInventory')
            
            SaveDeviceProper = DeviceRegisterUpload.objects.create(
                deviceusedepartment=deviceusedepartment, devicetype=devicetype, devicebrand=DeviceBrandProper, 
                deviceos=deviceos, devicecostofpurchase=devicecostofpurchase, devicename=devicename,
                devicemacaddress=devicemacaddress, devicelocation=devicelocation, deviceip=deviceip,
                devicestatus=devicestatus, staffUserID=staffUserID, CompanyUniqueCode=CompanyUniqueCode,
                deviceyearofpurchase=deviceyearofpurchase, user=user, devicedepreciationrate=depreciateRateReal,
                deviceid=uniqueId
            )
    
            try:
                SaveDeviceProper.save()
                messages.success(request, 'Device uploaded successfully')
                return redirect('DeviceInventory')
            except:
                messages.error(request, 'Device uploaded failed. Please Try again.')
                return redirect('DeviceInventory')
    except:
        messages.error(request, 'An error occured. Kindly try again.')
        return redirect('StaffMembers')
    allStaff = StaffDataSet.objects.get(id = id)

    
    if request.method == 'POST' and 'startAISession' in request.POST:
        print('clicked nowww')
        uniqueId = 'AI_Chat-' + get_random_string(length=5)
        createAIChat_Room = AIChat_Room.objects.create(uniqueId = uniqueId, companyID = request.user.last_name)
        createAIChat_Room.save()
        if createAIChat_Room:
            return redirect('AiChatPage')

    # allUploadedDevicesNotAssigned = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(staffUserID = 'None'))
    # form = UpdateDeviceUser(request.POST or None, instance = allUploadedDevicesNotAssigned)
    # if request.method == 'POST' and 'deviceToAssign' in request.POST and form.is_valid():
    #     print('selected existing user')
    #     form = UpdateDeviceUser(request.POST or None)
    #     deviceToAssign = request.POST['deviceToAssign']
    #     deviceToAssignMain = DeviceRegisterUpload.objects.get(deviceid = deviceToAssign)
    #     form = UpdateDeviceUser(request.POST or None)
    #     form.staffUserID = allStaff.StaffID
    #     form.save()
    #     DeviceRegisterForm(request.POST or None, instance = MainDeviceData)
    #       if request.POST and form.is_valid():
    #           form.save()
    #       if form.save():
    #           messages.success(request, 'Device data saved successfully')
    #       else:
    #           messages.success(request, 'Error saving device data')


    allUploadedDevices = DeviceRegisterUpload.objects.filter(user = request.user)
    allUploadedDevicesNotAssigned = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(staffUserID = 'None'))
    allSignUps = SignupForm.objects.all()
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'AllMaintenanceRequests':AllMaintenanceRequests, 'allSignUps':allSignUps, 'allStaff' : allStaff, 'allUploadedDevices' : allUploadedDevices, 'allUploadedDevicesNotAssigned':allUploadedDevicesNotAssigned}
    return render(request, 'userarea/staffdetails.html', context)


@login_required(login_url='Login')
def registerStaff(request, name):
    form = regStaff(request.POST)
    staffMembers = StaffDataSet.objects.all()
    context ={'form': form}
    # return render(request, 'userarea/post_form.html', context)
    return render(request, 'userarea/regstaffpage.html', context)



# EDIT USER SIGNUP DETAILS STARTS BELOW
@login_required(login_url='Login')
def EditUserSignupDetails(request, id):
    currentUser = SignupForm.objects.get(id = id)
    form = UserRegistrationForm(request.POST or None, instance = currentUser)
    if request.POST and form.is_valid():
        print('data validated!')
        userReg = form.save(commit=False)
        user = userReg.user
        user.username = form.cleaned_data['companyname']
        user.email = form.cleaned_data['email']
        user.save()
        userReg.save()
        if form.save():
            print('data saved!')
            messages.success(request, 'Your Company details have been updated successfully')
            return redirect('ProfilePage', pk=currentUser.id)
        else:
            messages.success(request, 'Error saving company details')
            return redirect('ProfilePage', pk=currentUser.id)


    allSignUps = SignupForm.objects.all()
    allProfileImages = UserProfileImage.objects.all().first
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'AllMaintenanceRequests':AllMaintenanceRequests, 'allProfileImages':allProfileImages, 'allSignUps':allSignUps, 'form' : form, 'currentUser' : currentUser}
    return render(request, 'userarea/editprofile.html', context)


def ProfilePage(request, pk):
    requestUser = SignupForm.objects.get(id = pk)
    allSignUps = SignupForm.objects.all()
    allUsers = User.objects.all()
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'AllMaintenanceRequests':AllMaintenanceRequests, 'allSignUps':allSignUps, 'allUsers':allUsers, 'requestUser':requestUser}
    return render(request, 'userarea/profilepage.html', context)


# DASHBOARD STARTS HERE
@login_required(login_url='Login')
def Dashboard(request):
    if request.method == "POST" and 'csv_file' in request.FILES:
        username = request.POST['username']
        savetimedata = request.POST['savetimedata']
        filedata = request.FILES.get('csv_file', False)
        
        if 'csv' not in str(filedata):
            messages.success(request, 'Wrong File Format. Please Use The Recommended CSV File.')
            return redirect('Dashboard')

        if request.FILES.get('csv_file') is None:
            messages.success(request, 'Device List Updated Failed! Please Select A File.')
            return redirect('Dashboard')
        
        if not request.POST['username']:
            messages.success(request, 'Device List Updated Failed! User Name Missing Login Again.')
            return redirect('Dashboard')

        form = uploadedDeviceData.objects.create(user = request.user, username = username, mainfile = filedata)
        randomNumber = random.randint(100, 9999)
        obj = uploadedDeviceData.objects.all().first()

        with open(obj.mainfile.path, 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                print(len(row))
                if i == 0:
                    pass
                elif len(row) < 21:
                # elif row[21] < 0:
                    messages.success(request, 'Upload Failed: Please Use The Sample CSV File Provided')
                    return redirect('Dashboard')
                # elif len(row) > 9:
                elif len(row) > 21:
                    today = date.today()
                                        
                    dateForWeekNumber = datetime.today()
                    weekNumber = dateForWeekNumber.isocalendar().week
                    uniqueId = 'Device-' + get_random_string(length=5)
                    randomNumberForStaff = random.randint(1000, 99999)
                    StaffUniqueId = 'Staff-' + request.user.username + str(randomNumberForStaff)
                    if row[21]:
                        depreciateRate = 2023 - int(row[21])                        
                    else:
                        depreciateRate = 2020
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

                    
                    if row[17] == '':
                        messages.error(request, 'Device user email address is missing, please fill in the email address and try again.')
                        return redirect('Dashboard')
                    
                    # if row[4] == '' or row[5] == '':
                    #     messages.error(request, "Device user's firstname or last name is missing. Please complete and try again")
                    #     return redirect('Dashboard')


                    AllStaffCheck = StaffDataSet.objects.filter(staff_email = row[17])
                    if AllStaffCheck:
                        print('email already exists')
                        messages.error(request, 'Sorry, a staff with an email address you are trying to upload has already been uploaded.')
                        return redirect('Dashboard')
                        

                    DeviceRegisterUpload.objects.create(
                        user = request.user,
                        deviceip = row[0],
                        devicename = row[1],
                        devicemacaddress = row[2],
                        devicenetworkadaptercompany = row[3],
                        deviceuserfirstname = row[4],
                        deviceuserlastname = row[5],
                        devicestatus = row[6],
                        deviceworkgroup = row[7],
                        deviceusedepartment = row[8],
                        deviceportnumber = row[9],
                        devicemultiplepacket = row[10],
                        index = row[11],
                        devicetype = row[12],
                        devicelocation = row[13],
                        devicebrand = row[14],
                        deviceos = row[15],
                        devicecostofpurchase = row[16],
                        deviceuseremail = row[17],
                        deviceuserphonenumber = row[18],
                        deviceuserdateofresumption = row[19],
                        deviceworkingcondition = row[20],
                        deviceyearofpurchase = row[21],
                        devicedepreciationrate = depreciateRateReal,
                        deviceid = uniqueId,
                        staffUserID = StaffUniqueId,
                        savetimedata = today.strftime("%B %d, %Y"),
                        registeredMonth = today.strftime("%b"),
                        weekNumberSaved = weekNumber,
                        CompanyUniqueCode = request.user.last_name
                    ),
                    # print(registeredMonth)
                    StaffDataSet.objects.create(
                        user = request.user,
                        StaffID = StaffUniqueId,
                        staff_firstname = row[4],
                        staff_lastname = row[5],
                        staff_phonenumber = row[18],
                        staff_location = row[13],
                        staff_email = row[17],
                        staff_role = row[8],
                        CompanyUniqueCode = request.user.last_name
                    )
                    
                    try:
                        checkUniqueUser =  User.objects.create_user(
                        username = row[17], email = StaffUniqueId, password =  StaffUniqueId, first_name = request.user.last_name, last_name = row[4] +' '+row[5]
                        )
                    except:
                        messages.error(request, 'Sorry, a staff with an email address you are trying to upload has already been uploaded.')
                        return redirect('Dashboard')
                    checkUniqueUser.save()

                else:
                    messages.error(request, 'Device List Updated Unsuccessfully: Please Fill CSV File And Upload Again')
                    return redirect('Dashboard')
            obj.save()
        messages.success(request, 'Device List Updated Successfully')
        return redirect('Dashboard')


    
    if request.method == 'POST' and 'deviceusedepartment' in request.POST:
        uniqueId = 'Device-' + get_random_string(length=5)
        today = date.today()
        dateForWeekNumber = datetime.today()
        weekNumber = dateForWeekNumber.isocalendar().week
        if request.POST['devicebrand']:
            randomNumber = random.randint(100, 9999)
            DeviceBrandProper = request.POST['devicebrand']+ '_' + str(randomNumber)
        else: 
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Brand.")
            return redirect('Dashboard')

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
            return redirect('Dashboard')
            
        deviceusedepartment = request.POST['deviceusedepartment']
        devicetype = request.POST['devicetype']
        devicebrand = request.POST['devicebrand']
        deviceos = request.POST['deviceos']
        devicecostofpurchase = request.POST['devicecostofpurchase']
        deviceyearofpurchase = request.POST['deviceyearofpurchase']
        devicename = request.POST['devicename']
        devicemacaddress = request.POST['devicemacaddress']
        devicelocation = request.POST['devicelocation']
        deviceip = request.POST['deviceip']
        devicestatus = request.POST['devicestatus']
        staffUserID = request.POST['staffUserID']
        CompanyUniqueCode = request.user.last_name
        user = request.user

        if not request.POST['deviceusedepartment']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Department.")
            return redirect('Dashboard')
        
        if not request.POST['devicemacaddress']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's MAC Address.")
            return redirect('Dashboard')
        
        if (DeviceRegisterUpload.objects.filter(Q(Q(devicename = request.POST['devicename']) & Q(user = request.user)))):
            messages.success(request, f'Upload Failed: the device: {devicename} already exists in your system. Please change the device name and try again')
            return redirect('DeviceInventory')
        
        if not request.POST['devicetype']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Type.")
            return redirect('Dashboard')
            

        if not request.POST['devicelocation']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Location.")
            return redirect('Dashboard')
        
        if not request.POST['devicestatus']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Working Condition.")
            return redirect('Dashboard')

        # if staffUserID:
        #     AllStaffMembers = StaffDataSet.objects.get(StaffID = staffUserID).staff_email
        #     print(AllStaffMembers)
        #     deviceuseremail = AllStaffMembers

        
        SaveDeviceProper = DeviceRegisterUpload(
            deviceusedepartment=deviceusedepartment, devicetype=devicetype, devicebrand=DeviceBrandProper, 
            deviceos=deviceos, devicecostofpurchase=devicecostofpurchase, devicename=devicename,
            devicemacaddress=devicemacaddress, devicelocation=devicelocation, deviceip=deviceip,
            devicestatus=devicestatus, staffUserID=staffUserID, CompanyUniqueCode=CompanyUniqueCode,
            deviceyearofpurchase=deviceyearofpurchase, user=user, devicedepreciationrate=depreciateRateReal,
            deviceid=uniqueId, savetimedata = today.strftime("%B %d, %Y"), registeredMonth = today.strftime("%b"), weekNumberSaved = weekNumber
        )

        # SAVE FAULTY OR CRITICAL DEVICES 
        if request.POST['devicestatus'] == 'Faulty' or request.POST['devicestatus'] == 'Critical':
            CompanyFaultyDevicesForm = CompanyFaultyDevices(user = request.user, deviceID = uniqueId, month = today.strftime("%b"), year = today.strftime("%B %d, %Y"), CompanyUniqueCode = request.user.last_name)
            CompanyFaultyDevicesForm.save()             
        
        
        try:
            SaveDeviceProper.save()
            messages.success(request, 'Device uploaded successfully')
            return redirect('Dashboard')
        except:
            messages.error('Device uploaded failed. Please Try again.')
            redirect('Dashboard')

    
    if request.method == 'POST' and 'startAISession' in request.POST:
        print('clicked nowww')
        uniqueId = 'AI_Chat-' + get_random_string(length=5)
        createAIChat_Room = AIChat_Room.objects.create(uniqueId = uniqueId, companyID = request.user.last_name)
        createAIChat_Room.save()
        if createAIChat_Room:
            return redirect('AiChatPage')
    
    allDevicesMonthPre = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = request.user.last_name)
    AllCompanyFaultyDevices = CompanyFaultyDevices.objects.filter(CompanyUniqueCode = request.user.last_name)
    JanDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'Jan'))
    FebDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'Feb'))
    MarDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'Mar'))
    AprDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'Apr'))
    MayDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'May'))
    JunDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'Jun'))
    JulDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'Jul'))
    # print('JunDevices')
    # print(JulDevices)
    AugDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'Aug'))
    SeptDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'Sep'))
    OctDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'Oct'))
    NovDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'Nov'))
    DecDevices = CompanyFaultyDevices.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(month = 'Dec'))

    Amounts = ['100,000', '200,000', '300,000', '400,000', '500,000']

    # dataMain = [JanDevices1, FebDevices1, MarDevices1, AprDevices1, MayDevices1, JuneDevices1, JulyDevices1, AugDevices1, SeptDevices1, OctDevices1, NovDevices1, DecDevices1]
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    AllMaintenancesCount = MaintenanceRequest.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(MaintainStatus = 'Ongoing') & Q(MaintainStatus = 'Pending')).count()
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
        


    allUploadedDevices = DeviceRegisterUpload.objects.filter(user = request.user)
    allUploadedDevicesCount = allUploadedDevices.count()
    AllStaffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.last_name)
    AllStaffMembersByID = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.last_name).order_by('-id')
    FirstStaffMembers = AllStaffMembersByID[:3]
    AllMaintenanceRequestID = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name).order_by('-id')
    FirstThreeMaintenanceRequest = AllMaintenanceRequestID[:4]
    StaffCount = AllStaffMembers.count()
    DeviceRegister1 = DeviceRegisterUpload.objects.filter(user=request.user)
    badSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Faulty') & Q(user = request.user))
    badSystems = badSystems1.count()
    workingSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(user = request.user))
    workingSystems = workingSystems1.count()
    warningSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Critical') & Q(user = request.user))
    warningSystems = warningSystems1.count()
    AllLaptops = DeviceRegisterUpload.objects.filter(Q(devicetype = 'Laptop' or 'laptop') & Q(user = request.user))
    AllLaptopsCount = AllLaptops.count()
    AllDesktops = DeviceRegisterUpload.objects.filter(Q(devicetype = 'Desktop' or 'desktop') & Q(user = request.user))
    AllDesktopsCount = AllDesktops.count()
    labels = ['Laptops', 'Desktops']
    data = [AllLaptopsCount, AllDesktopsCount]
    thisYear = datetime.today().year
    allSignUps = SignupForm.objects.filter(user = request.user)
    allUsers = User.objects.all()
    allSignupsForUpdatePopup = SignupForm.objects.filter(email = request.user.email)
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'AllMaintenanceRequests':AllMaintenanceRequests, 'allSignupsForUpdatePopup':allSignupsForUpdatePopup, 
    'AllStaffMembers':AllStaffMembers,'allUsers':allUsers, 'allSignUps':allSignUps, 'labels':labels,'thisYear':thisYear, 'data':data, 
    'allUploadedDevices':allUploadedDevices,'badSystems':badSystems, 'allUploadedDevicesCount':allUploadedDevicesCount, 'StaffCount':StaffCount,
    'JanDevices':JanDevices, 'FebDevices':FebDevices, 'AugDevices':AugDevices, 'SeptDevices':SeptDevices, 'workingSystems':workingSystems,
    'OctDevices':OctDevices, 'NovDevices':NovDevices, 'DecDevices':DecDevices, 'MarDevices':MarDevices, 
    'AprDevices':AprDevices, 'MayDevices':MayDevices,'JunDevices':JunDevices, 'JulDevices':JulDevices, 'AllLaptopsCount':AllLaptopsCount,
    'labels':labels, 'FirstThreeMaintenanceRequest':FirstThreeMaintenanceRequest, 'AllDesktopsCount': AllDesktopsCount,
    'allSignUps':allSignUps, 'allUsers':allUsers, 'AllMaintenancesCount':AllMaintenancesCount, 'FirstStaffMembers':FirstStaffMembers,
    }
    return render(request, 'userarea/dashboard.html', context)



# EDIT STAFF DETAILS STARTS BELOW
def EditStaff(request, staffid):
    # user = request.user
    currentStaff = StaffDataSet.objects.get(id = staffid)
    form = staffForm(request.POST or None, instance = currentStaff)
    if request.POST and form.is_valid():
        print('request is valid')
        form.save()
        return redirect('StaffMembers')
        # form.save(commit=False)
        # allUserNow = User.objects.all()
        # for data in allUserNow:
        #     print(data)
        #     if data.username == currentStaff.staff_email:
        #         print('currentStaff.staff_email')
            # if data.email == currentStaff.StaffID:
                # data = data.user
                # data.username = form.cleaned_data['staff_email']
                # data.save()
                # StaffReg.save()
                # if form.save():
                #     messages.success(request, 'Staff details edited successfully')
                #     return redirect('StaffMembers')
                # else:
                #     messages.success(request, 'Error saving staff details')            
            # else:
            #     messages.success(request, 'An error occured. Please try again')
            #     return redirect('StaffMembers')

    allUsers = User.objects.all()
    context = {'allUsers':allUsers, 'form' : form, 'currentStaff' : currentStaff}
    return render(request, 'userarea/editStaffDetails.html', context)


def Logout(request):
    # MainLoginStatus = LoginStatus.objects.filter(email = request.user.last_name)
    # MainLoginStatus.delete()
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('Login')



@login_required(login_url='Login')
def DisplayUploadedFile(request, file):
    csv_fp = open(f'/media/uploadedfiles/{file}', 'r')
    reader = csv.DictReader(csv_fp)
    headers = [col for col in reader.fieldnames]
    out = [row for row in reader]
    return render(request, 'userarea/formstext.html', {'data' : out, 'headers' : headers})



@login_required(login_url='Login')
def AllUploadedFilesList(request, userdata):
    deviceslist = uploadedDeviceData.objects.filter(Q(username = userdata) & Q(user = request.user))
    context = {'deviceslist': deviceslist}
    return render(request,'userarea/alluploadedfiles.html', context)


@login_required(login_url='Login')
def downloadfile(request):
    return render(request,'userarea/uploaddevices.html')


@login_required(login_url='Login')
def fileUpload(request):
    form = DeviceRegisterForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = DeviceRegisterForm()
    return render(request, 'userarea/formstext.html', {'form': form})


# FULL SAMPLE CSV FILE
@login_required(login_url='Login')
def downloadSampleFile(request):
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename =  ITSA Inventory Device Upload Sample File.csv'
    writer = csv.writer(response)
    writer.writerow(['Device IP Address', 'Device Name*', 'Device MAC Address*', 'Device Network Adapter Company',
     'Device User First Name*', 'Device User Last Name*', 'Device Status', 'Company Name', 'Device Use Department*', 
     'Device Port Number', 'Device Multiple Packet', 'Device Index', 'Device Type',
     'Device Location*', 'Device Brand', 'Device Operating System*', 'Device Cost Of Purchase*','Device User Email Address*', 
     'Device User Phone Number', 'Device User Job Resumption Date', 'Device Working Status', 'Device Year Of Purchase*'
     ])
    writer.writerow(['20.20.0.27', 'DESKTOP-7687TC8', '20-10-7A-4E-9F-46', 'Gemtek Technology Co., Ltd.', 'John', 'Doe', 'on', 
    'IT Service Desk Africa', 'IT Department', '433', 'Nil', '1', 'Laptop', 'Aba Abia State', 'Toshiba', 
    'Windows 10 Pro', 'N100, 000', 'johndoe@itservicedeskafrica.com', '0701 156 7240', '2020', 'Good', '2023'])
    return response



# SAMPLE LIST TO SEE HOW HEADERS ARE ON CSV FILE
@login_required(login_url='Login')
def downloadSampleCSV(request):
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename = ITSA Inventory CSV Sample File.csv'
    writer = csv.writer(response)
    writer.writerow(['Device IP Address', 'Device Name', 'Device MAC Address', 'Device Network Adapter Company',
     'Device User First Name', 'Device User Last Name', 'Device Status', 'Company Name', 'Device Use Department', 
     'Device Port Number', 'Device Multiple Packet', 'Device Index', 'Device Type',
     'Device Location', 'Device Brand', 'Device Operating System', 'Device Cost Of Purchase','Device User Email Address', 
     'Device User Phone Number', 'Device User Job Resumption Date', 'Device Working Status', 'Device Year Of Purchase'
     ])
    # writer.writerow(['Kindly Delete This And Paste From This Field'])
    return response



@login_required(login_url='Login')
def SearchResult(request):
    return render(request, 'userarea/searchresult.html')



# @login_required(login_url='Login')
def Searchresult(request):
    print('seaching...')
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if request.method == 'GET':
        print(q)
        deviceSearch = DeviceRegisterUpload.objects.filter(
       Q(Q(deviceid__icontains = q) | 
        Q(deviceuserfirstname__icontains = q) |
        Q(deviceuserlastname__icontains = q) |
        Q(devicemacaddress__icontains = q) |
        Q(deviceusedepartment__icontains = q) |
        Q(devicestatus__icontains = q) |
        Q(devicebrand__icontains = q) |
        Q(created_at__icontains = q) |
        Q(devicetype__icontains = q) |
        Q(devicelocation__icontains = q) |
        Q(savetimedata__icontains = q) |
        Q(weekNumberSaved__icontains = q)
    ) & Q(user = request.user))
# Q(devicestatus = 'Faulty') & Q(user = request.user)
    deviceSearchCount = deviceSearch.count()
    thisYear = datetime.today().year
    today = datetime.today()
    dateNow = datetime.now()
    month1 = dateNow.strftime("%b")
    # month1 = 'April'
    print("Current Month Full Name:", month1)
    print("dateNow", dateNow)
    print("today", today)
    date = datetime.today()
    weekNumber = date.isocalendar().week
    print('this week number:', weekNumber)
    allUsers = User.objects.all()
    
    context = {'allUsers':allUsers, 'deviceSearch': deviceSearch, 'deviceSearchCount':deviceSearchCount}
    return render(request, 'userarea/searchresult.html', context)



def ScanNetwork(request):
    if request.method == "POST" and 'csv_file' in request.FILES:
        username = request.POST['username']
        savetimedata = request.POST['savetimedata']
        filedata = request.FILES.get('csv_file', False)
        
        print(str(username))
        print(str(filedata))
        if 'csv' not in str(filedata):
            messages.success(request, 'Wrong File Format. Please Use The Recommended CSV File.')
            return redirect('ScanNetwork')

        if request.FILES.get('csv_file') is None:
            messages.success(request, 'Device List Updated Failed! Please Select A File.')
            return redirect('ScanNetwork')
        
        if not request.POST['username']:
            messages.success(request, 'Device List Updated Failed! User Name Missing Login Again.')
            return redirect('ScanNetwork')

        form = uploadedDeviceData.objects.create(user = request.user, username = username, mainfile = filedata)
        obj = uploadedDeviceData.objects.all().first()
        randomNumber = random.randint(100, 9999)

        with open(obj.mainfile.path, 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    pass
                elif len(row) < 21:
                # elif row[21] < 0:
                    messages.success(request, 'Upload Failed: Please Use The Sample CSV File Provided')
                    return redirect('Dashboard')
                # elif len(row) > 9:
                elif len(row) > 21:
                    # print(len(row))
                    today = date.today()
                                        
                    dateForWeekNumber = datetime.today()
                    weekNumber = dateForWeekNumber.isocalendar().week
                    uniqueId = 'Device-' + get_random_string(length=5)
                    # DeviceBrandProper = row[14]+'_'+str(randomNumber)
                    randomNumberForStaff = random.randint(1000, 99999)
                    StaffUniqueId = 'Staff-' + request.user.username + str(randomNumberForStaff)
                    if row[21]:
                        depreciateRate = 2023 - int(row[21])                        
                    else:
                        depreciateRate = 2020
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
                    
                    if row[17] == '':
                        messages.error(request, 'Device user email address is missing, please fill in the email address and try again.')
                        return redirect('Dashboard')
                    
                    # if row[4] == '' or row[5] == '':
                    #     messages.error(request, "Device user's firstname or last name is missing. Please complete and try again")
                    #     return redirect('Dashboard')

                    

                    AllStaffCheck = StaffDataSet.objects.filter(staff_email = row[17])
                    print(AllStaffCheck)
                    if AllStaffCheck:
                        print('email already exists')
                        messages.error(request, 'Sorry, a staff with an email address you are trying to upload has already been uploaded.')
                        return redirect('Dashboard')
                        
                    DeviceRegisterUpload.objects.create(
                        user = request.user,
                        deviceip = row[0],
                        devicename = row[1],
                        devicemacaddress = row[2],
                        devicenetworkadaptercompany = row[3],
                        deviceuserfirstname = row[4],
                        deviceuserlastname = row[5],
                        devicestatus = row[6],
                        deviceworkgroup = row[7],
                        deviceusedepartment = row[8],
                        deviceportnumber = row[9],
                        devicemultiplepacket = row[10],
                        index = row[11],
                        devicetype = row[12],
                        devicelocation = row[13],
                        devicebrand = row[14],
                        deviceos = row[15],
                        devicecostofpurchase = row[16],
                        deviceuseremail = row[17],
                        deviceuserphonenumber = row[18],
                        deviceuserdateofresumption = row[19],
                        deviceworkingcondition = row[20],
                        deviceyearofpurchase = row[21],
                        devicedepreciationrate = depreciateRateReal,
                        deviceid = uniqueId,
                        staffUserID = StaffUniqueId,
                        savetimedata = today.strftime("%B %d, %Y"),
                        registeredMonth = today.strftime("%b"),
                        weekNumberSaved = weekNumber,
                        CompanyUniqueCode = request.user.last_name
                    ),
                    StaffDataSet.objects.create(
                        user = request.user,
                        StaffID = StaffUniqueId,
                        staff_firstname = row[4],
                        staff_lastname = row[5],
                        staff_phonenumber = row[18],
                        staff_location = row[13],
                        staff_email = row[17],
                        staff_role = row[8],
                        # staff_DeviceStatus = row[6],
                        CompanyUniqueCode = request.user.last_name
                        # CompanyUniqueCode = request.user.last_name
                    )
                    try:
                        checkUniqueUser =  User.objects.create_user(
                        username = row[17], email = StaffUniqueId, password =  StaffUniqueId, first_name = request.user.last_name, last_name = row[4] +' '+row[5]
                        )
                    except:
                         checkUniqueUserMain = User.objects.filter(username = row[17])
                         print(checkUniqueUserMain)
                         messages.error(request, 'Sorry, a staff with an email address you are trying to upload has already been uploaded.')
                         return redirect('ScanNetwork')
                    checkUniqueUser.save()
                else:
                    messages.error(request, 'Device List Updated Unsuccessfully')
                    return redirect('ScanNetwork')
            obj.save()
        messages.success(request, 'Device List Updated Successfully')
        return redirect('DeviceInventory')
    return render(request, 'userarea/scannetwork.html')


# FULL SAMPLE CSV FILE
def downloadSampleFile(request):
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename =  Device Upload Sample File.csv'
    writer = csv.writer(response)
    writer.writerow(['Device IP Address', 'Device Name', 'Device MAC Address', 'Device Network Adapter Company',
     'Device User First Name', 'Device User Last Name', 'Device Status', 'Company Name', 'Device Use Department', 
     'Device Port Number', 'Device Multiple Packet', 'Device Index', 'Device Type',
     'Device Location', 'Device Brand', 'Device Operating System', 'Device Cost Of Purchase','Device User Email Address', 
     'Device User Phone Number', 'Device User Job Resumption Date', 'Device Condition', 'Device Year Of Purchase'
     ])
    writer.writerow(['20.20.0.27', 'DESKTOP-7687TC8', '20-10-7A-4E-9F-46', 'Gemtek Technology Co., Ltd.', 'John', 'Doe', 'Working', 
    'IT Service Desk Africa', 'IT Department', '433', 'Nil', '1', 'Laptop', 'Lagos State', 'Toshiba', 
    'Windows 10 Pro', '100,000', 'johndoe@itservicedeskafrica.com', '0701 156 7240', '2020', 'Good', '2023'])
    return response



# SAMPLE LIST TO SEE HOW HEADERS ARE ON CSV FILE
def downloadSampleCSVHeaders(request):
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename = CSV Sample File.csv'
    writer = csv.writer(response)
    writer.writerow(['Device IP Address', 'Device Name', 'Device MAC Address', 'Device Network Adapter Company',
     'Device User First Name', 'Device User Last Name', 'Device Status', 'Company Name', 'Device Department', 
     'Device Port Number', 'Device Multiple Packet', 'Device Index', 'Device Type',
     'Device Location', 'Device Brand', 'Device Operating System', 'Device Cost Of Purchase','Device User Email Address', 
     'Device User Phone Number', 'Device User Job Resumption Date', 'Device Working Status', 'Device Year Of Purchase'
     ])
    # writer.writerow(['Kindly Delete This And Paste From This Field'])
    return response



def DeleteDevice(request, pk):
    deviceToDelete = DeviceRegisterUpload.objects.get(id=pk)
    deviceToDeleteName = deviceToDelete.devicename
    deviceToDeleteMAC = deviceToDelete.devicemacaddress
    deviceToDeleteID = deviceToDelete.deviceid
    deviceToDeleteBrand = deviceToDelete.devicebrand
    deviceToDeleteUniqueCode = deviceToDelete.CompanyUniqueCode
    form = DeletedDevices(        
        deletedDeviceName = deviceToDeleteName, deletedDeviceMAC_ID = deviceToDeleteMAC, 
        deletedDeviceID = deviceToDeleteID, deletedDeviceBrand = deviceToDeleteBrand, 
        deletedDeviceCompanyUniqueCode = deviceToDeleteUniqueCode, user = request.user,
    )

    form.save()
    if form:
        deviceToDelete.delete()

    else:
        messages.success(request, 'An error occured while deleting the device. Please try again or contact support for assistance')
        return redirect('DeviceInventory')

    messages.success(request, 'Device Successfully Deleted!')
    return redirect('DeviceInventory')
    # return render(request, 'userarea/deviceinventory.html')


def AllDeviceDelete(request):
    AllDevices = DeviceRegisterUpload.objects.filter(user = request.user)
    messages.error(request, 'All devices have been deleted successfully!')
    # AllDevices.delete()
    return redirect('DeviceInventory')



def DeleteStaff(request, pk):
    staffToDeleteEmail = StaffDataSet.objects.get(id=pk).staff_email
    staffToDelete = StaffDataSet.objects.get(id=pk)
    staffToDelete.delete()
    try:
        getStaffUser = User.objects.get(username = staffToDeleteEmail)
        getStaffUser.delete()
    except:
        print('Staff admin account was not found while trying to delete staff')
    messages.success(request, 'Staff Details Successfully Deleted!')
    return redirect('StaffMembers')
    # return render(request, 'userarea/deviceinventory.html')



def EditProfileImg(request):
    if request.method == 'POST' and 'profilepicture' in request.POST:
        profilepicture = request.FILES['profilepicture']
        UserProfileImage.objects.create(user = request.user, userReg = request.user.username, profilepicture = Profilepicture)
    return render(request, 'userarea/updateimage.html')



def UploadProfileImg(request, pk):
    allSignUps = SignupForm.objects.filter(id = pk)
    if request.method == 'POST':
        profilepictureproper = request.FILES['profilepicture']

        if not request.FILES['profilepicture']:
            messages.error(request, 'Error saving company profile image')

        ProfileImgForm = UserProfileImage.objects.create(user = request.user, userReg = request.user.username, 
        profilepicture = profilepictureproper)
        ProfileImgForm.save()
    # else:
    #     messages.success(request, 'Error saving company profile image')

    # messages.success(request, 'Error saving company profile image')
    allUsers = User.objects.all()
    allProfileImages2 = UserProfileImage.objects.all()
    allProfileImages = UserProfileImage.objects.filter(userReg = request.user.username).first()
    context = {'allProfileImages2':allProfileImages2, 'allProfileImages':allProfileImages, 'allUsers':allUsers, 'allSignUps': allSignUps}
    return render(request, 'userarea/updateimage.html', context)


def TestPage(request):
    allProfileImages2 = UserProfileImage.objects.all()
    allProfileImages = UserProfileImage.objects.filter(userReg = request.user.username).first()
    context = {'allProfileImages2':allProfileImages2, 'allProfileImages':allProfileImages}
    return render(request, 'userarea/test.html', context)


# FIND ALL INSTALLED APPS ON THIS PC
def AllInstalledApp(request):
    item = winapps.list_installed
    print(item)
    context = {'item':item}
    return render(request, 'userarea/test.html', context)


# ACCORDING TO CHAT GPT : FOR A LINUS MACHINE, RUN CODE BELOW:

import subprocess

# def get_installed_applications():
#     try:
#         # Check for Debian-based systems (e.g., Ubuntu)
#         debian_cmd = "dpkg-query -l | grep '^ii' | awk '{print $2}'"
#         debian_apps = subprocess.check_output(debian_cmd, shell=True, universal_newlines=True)

#         # Check for Red Hat-based systems (e.g., CentOS)
#         redhat_cmd = "rpm -qa"wi
#         redhat_apps = subprocess.check_output(redhat_cmd, shell=True, universal_newlines=True)

#         # Combine the lists and remove duplicates
#         all_apps = set(debian_apps.splitlines() + redhat_apps.splitlines())

#         return sorted(all_apps)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []

# if __name__ == "__main__":
#     installed_apps = get_installed_applications()
#     if installed_apps:
#         print("Installed applications:")
#         for app in installed_apps:
#             print(app)
#     else:
#         print("No installed applications found.")


# ACCORDING TO CHAT GPT : FOR A LINUS MACHINE, RUN CODE ABOVE:


def AllInstalledSoftwares(request):
    # item = winapps.list_installed
    allSignUps = SignupForm.objects.all()
    
    # Data = subprocess.check_output(args)
    Data = subprocess.check_output(['wmic', 'product', 'get', 'name'])
    a = str(Data)
    for i in range(len(a)):
        RawListOfApp = a.split("\\r\\r\\n")[6:]
        RawListOfAppName = RawListOfApp[6:]
    context = {'item':RawListOfAppName, 'allSignUps':allSignUps}
    return render(request, 'userarea/allinstalledapp.html', context)



# Franklin-franklin.i@itservicedeskafrica.com
def UpdateCompanyDetails(request, email, name):
    WorkingUsers = User.objects.get(email=email)
    if request.method == 'POST' :
        user = request.user
        companyname = request.POST['companyname']
        email = request.POST['email']
        phone = request.POST['phone']
        city = request.POST['city']
        country = request.POST['country']
        address = request.POST['address']
        password = request.POST['password']
        repassword = request.POST['repassword']

        companyUniqueID = request.POST['email']   

        if not request.POST['companyname']:
            messages.error(request, 'Account update failed!: Enter Your Company Name')
            # return redirect('UpdateCompanyDetails')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

        if not request.POST['email']:
            messages.error(request, 'Account update failed!: Enter Your Company Email Address')
            # return redirect('UpdateCompanyDetails')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

        if not request.POST['phone']:
            messages.error(request, 'Account update failed!: Enter Your Company City Location')
            # return redirect('UpdateCompanyDetails')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

        if not request.POST['country']:
            messages.error(request, 'Account update failed!: Enter Your Company Country Location')
            # return redirect('UpdateCompanyDetails')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

        if not request.POST['address']:
            messages.error(request, 'Account update failed!: Enter Your Company Address')
            # return redirect('UpdateCompanyDetails')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

        if not request.POST['password']:
            messages.error(request, 'Account update failed!: Enter Your Password')
            # return redirect('UpdateCompanyDetails')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        
        if not request.POST['repassword']:
            messages.error(request, 'Account update failed!: Enter the retype password box to validate your password.')
            # return redirect('UpdateCompanyDetails')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

        if (password != repassword):
            messages.error(request, 'Passwords Do Not Match!')
            # return redirect('UpdateCompanyDetails')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)


        data = SignupForm.objects.filter(companyname=companyname)
        # UserData = User.objects.filter(username=companyname)
        if data:
            messages.error(request, 'Sorry, Company Name Is Already Taken, Please Use Another Company Name')
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

        else:
            messages.success(request, 'Account updated successful')
            createUpdatdUser = SignupForm.objects.create(
            user = request.user, companyname = companyname, email= email, phone = phone,
            city = city, country = country, password = password, repassword = repassword,
            address = address, companyUniqueID = companyUniqueID)
            createUpdatdUser.save()            
            return redirect('Dashboard')


    context = {'WorkingUsers':WorkingUsers}
    return render(request, 'userarea/updatedetails.html', context)



@login_required(login_url='Login')
def SubAdmin(request):
    AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    AllStaffIDArr = []
    AllStaffIDArrNew = []
    SubAdminDepts = list(SubAdminModel.objects.all().values_list('subadmin_dept', flat=True))
    AllStaffMembers = StaffDataSet.objects.all()
    AllSubAdminModelCount = SubAdminModel.objects.filter(CompanyUniqueCode = request.user.last_name).count()
    AllSubAdminModel = SubAdminModel.objects.filter(CompanyUniqueCode = request.user.last_name)

    if request.method == 'POST' and 'allSubAdminArr' in request.POST:
        allSubAdminArr = request.POST['allSubAdminArr'].split(',')
        print(allSubAdminArr)

        if allSubAdminArr == ['']:
            messages.error(request, 'An error occured, please try again.')
            return redirect('SubAdmin')

        for a in allSubAdminArr:
            SubAdminModelExit = SubAdminModel.objects.filter(StaffID = a)
            AllStaffID = list(StaffDataSet.objects.filter(StaffID = a).values_list('staff_role', flat=True))
            AllStaffIDArrNew.append(AllStaffID)


        for i in AllStaffIDArrNew:
            AllStaffIDArrNewCount = AllStaffIDArrNew.count(i) > 1

        if SubAdminModelExit:
            messages.error(request, 'A staff you selected already exists as a sub-Admin. Please select a non Sub-Admin to assign.')
            return redirect('SubAdmin')

        for a in allSubAdminArr:
            AllStaffID22 = list(StaffDataSet.objects.filter(StaffID = a).values_list('staff_role', flat=True))
            for i in AllStaffID22:
                for q in SubAdminDepts:
                    if q == i:
                        messages.error(request, 'You selected a staff whose department already has a subadmin, please delete existing subadmin before reassigning.')
                        return redirect('SubAdmin')

            
        if AllStaffIDArrNewCount is True:
            messages.error(request, 'You selected two staff members from the same department. Please select one staff member per department.')
            return redirect('SubAdmin')
    

        if AllStaffIDArrNewCount is False:
            for a in allSubAdminArr:
                AllStaffID = StaffDataSet.objects.filter(StaffID = a).values_list('staff_role', flat=True)
                SubAdminModel.objects.create(StaffID = a, subadmin_dept = AllStaffID, user = request.user, CompanyUniqueCode = request.user.last_name)
                AllSubAdminModelCount = SubAdminModel.objects.filter(CompanyUniqueCode = request.user.last_name).count()
                

    context = {'AllSubAdminModelCount':AllSubAdminModelCount, 'AllMaintenanceRequests':AllMaintenanceRequests, 'AllStaffMembers':AllStaffMembers, 'AllSubAdminModel':AllSubAdminModel}
    return render(request, 'userarea/subadmin.html', context)





def DeletSubAdmin(request, pk):
    SubAdminToDelete = SubAdminModel.objects.get(id = pk)
    SubAdminToDelete.delete()
    messages.error(request, 'Sub-Admin has been deleted')
    return redirect('SubAdmin')



# SAMPLE LIST TO SEE HOW HEADERS ARE ON CSV FILE
@login_required(login_url='Login')
def SampleFileForStaffAD(request):
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename = Staff AD Sample File.csv'
    writer = csv.writer(response)
    writer.writerow(['staff name', 'staff email address'])
    writer.writerow(['Franklin Isaac', 'franklin.i@itservicedeskafrica.com'])
    writer.writerow(['Jane Doe', 'jane.d@itservicedeskafrica.com'])
    writer.writerow(['John Doe', 'john.d@itservicedeskafrica.com'])
    return response


def errorpagevisist(request):
    return render(request, '404.html')





def maintenenceRequestNotification(request, myCompanyEmailAddress, myCompanyName, MaintainRequester, MaintainPriorityStatus, MaintainDeviceMAC, MaintainType, MaintainRequestDescription):
    recipient_list = [myCompanyEmailAddress, 'franklin.i@itservicedeskafrica.com', 'chinedu.o@itservicedeskafrica.com']
    if (MaintainPriorityStatus == 'Low'):         
        ResponseTime = 'Five (5) Business Days'
    elif (MaintainPriorityStatus == 'Medium'):         
        ResponseTime = 'Fourty Eight (48) Working Hours'
    elif (MaintainPriorityStatus == 'High'):         
        ResponseTime = 'Eight (8) Wordking Hours'

    context = {'myCompanyName':myCompanyName, 'ResponseTime':ResponseTime, 'MaintainRequester':MaintainRequester, 'MaintainPriorityStatus':MaintainPriorityStatus, 'MaintainDeviceMAC':MaintainDeviceMAC, 'MaintainType':MaintainType, 'MaintainRequestDescription':MaintainRequestDescription}
    html_message = render_to_string("mailouts/adminmaintenancereqmail.html", context=context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject = "ADMIN DEVICE MAINTENANCE REQUEST ALERT - DHMS.", 
        body = plain_message,
        from_email = 'dhmsinventoryapp@gmail.com',
        to= recipient_list
        )

    message.attach_alternative(html_message, "text/html")
    message.send()

    if message:
        print('Sent a confirmation email')
    else:
        messages.error(request, f'Problem sending email to {myCompanyEmailAddress}, check if you typed it correctly')

