# from site import USER_BASE
from django.urls import reverse
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
import csv
from django.db.models import Q
from useronboard.models import SignupForm, UserProfileImage
from datetime import datetime
from datetime import date
from django.utils.crypto import get_random_string
import json
from django.contrib.auth.models import User
# import winapps
import random

# import datetime; 

# Create your views here.


@login_required(login_url='Login')
def NavBar(request):
    # allSignUps = SignupForm.objects.all()
    allSignUps = SignupForm.objects.filter(user = request.user)
    context = {'allSignUps': allSignUps}
    return render(request, 'general.html', context)




@login_required(login_url='Login')
def Reports(request):
    allUsers = User.objects.all()
    allSignUps = SignupForm.objects.all()
    allDevices = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = request.user.email)
    allDevicesCount = allDevices.count()
    allDevicesMonthPre = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = request.user.email)
    allDevicesMonth = allDevicesMonthPre.values_list('registeredMonth')
    # allDevicesMonth = DeviceRegisterUpload.objects.values_list('registeredMonth')
    JanDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'Jan'))
    JanDevices1 = JanDevices.count()
    FebDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'Feb'))
    FebDevices1 = FebDevices.count()
    MarDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'Mar'))
    MarDevices1 = MarDevices.count()
    AprDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'Apr'))
    AprDevices1 = AprDevices.count()
    MayDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'May'))
    MayDevices1 = MayDevices.count()
    JuneDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'Jun'))
    JuneDevices1 = JuneDevices.count()
    JulyDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'Jul'))
    JulyDevices1 = JulyDevices.count()
    AugDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'Aug'))
    AugDevices1 = AugDevices.count()
    SeptDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'Sep'))
    SeptDevices1 = SeptDevices.count()
    OctDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'Oct'))
    OctDevices1 = OctDevices.count()
    NovDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'Nov'))
    NovDevices1 = NovDevices.count()
    DecDevices = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(registeredMonth = 'Dec'))
    DecDevices1 = DecDevices.count()

    Amounts = ['100,000', '200,000', '300,000', '400,000', '500,000']

    data = [JanDevices1, FebDevices1, MarDevices1, AprDevices1, MayDevices1, JuneDevices1, JulyDevices1, AugDevices1, SeptDevices1, OctDevices1, NovDevices1, DecDevices1]
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    AllMaintenances = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.email).count()

    context = {'JanDevices':JanDevices, 'FebDevices':FebDevices, 'AugDevices':AugDevices, 'SeptDevices':SeptDevices, 
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
    context = {'allSignUps':allSignUps, 'allUsers':allUsers, 'allProfileImages':allProfileImages}
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
                    'MaintainDeviceLocation', 'MaintainStatus', 'MaintainDeviceUserFirstname', 'MaintainDeviceUserLastname', 'MaintainRequester', 'MaintainRequestID', 
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
        print(len(deviceToDeleteArr))
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



    allMaintains = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.email) 
    # allMaintains = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name) 
    allMaintainsCount = allMaintains.count()

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
    context = {'allOngoingRequestsCount':allOngoingRequestsCount, 'allCompletedRequestsCount':allCompletedRequestsCount, 'allCanceledRequestsCount':allCanceledRequestsCount, 'allSignUps':allSignUps, 'allUsers':allUsers, 'allProfileImages':allProfileImages, 'allMaintains':allMaintains, 'allMaintainsCount':allMaintainsCount, 'numberOfDevicesPerPage':numberOfDevicesPerPage}
    return render(request, 'userarea/maintainance.html', context)



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
    AllMaintainDevice = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.email)
    # AllMaintainDevice = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
    context = {'AllCommments':AllCommments, 'AllMaintainDevice':AllMaintainDevice, 'currentDevice':currentDevice}
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
    context = {'form':form, 'selectedRequest':selectedRequest}
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
    context = {'allSignUps':allSignUps, 'allUsers':allUsers, 'allProfileImages':allProfileImages}
    return render(request, 'userarea/settings.html', context)


@login_required(login_url='Login')
def DeviceInventory(request):
    if request.method == 'POST' and 'deviceusedepartment' in request.POST:
        uniqueId = 'Device-' + get_random_string(length=5)
        if request.POST['devicebrand']:
            randomNumber = random.randint(100, 9999)
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
        staffUserID = request.POST['staffUserID']
        CompanyUniqueCode = request.POST['CompanyUniqueCode']
        # CompanyUniqueCode = request.POST['CompanyUniqueCode']
        user = request.user

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


    # CSV UPLOAD STARTS HERE
    if request.method == "POST" and 'csv_file' in request.FILES:
        username = request.POST['username']
        filedata = request.FILES.get('csv_file', False)
        
        print(str(username))
        print(str(filedata))
        if 'csv' not in str(filedata):
            messages.success(request, 'Wrong File Format. Please Use The Recommended CSV File.')
            return redirect('DeviceInventory')

        if request.FILES.get('csv_file') is None:
            messages.success(request, 'Device List Updated Failed! Please Select A File.')
            return redirect('DeviceInventory')
        
        if not request.POST['username']:
            messages.success(request, 'Device List Updated Failed! User Name Missing Login Again.')
            return redirect('DeviceInventory')

        form = uploadedDeviceData.objects.create(username = username, mainfile = filedata)
        obj = uploadedDeviceData.objects.all().first()

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
                    today = date.today()

                    dateForWeekNumber = datetime.today()
                    randomNumber = random.randint(100, 9999)
                    weekNumber = dateForWeekNumber.isocalendar().week
                    randomNumberForStaff = random.randint(1000, 99999)
                    StaffUniqueId = 'Staff-' + request.user.username + str(randomNumberForStaff)
                    # ('Samsung·', 3501)
                    uniqueId = 'Device-' + get_random_string(length=5)
                    # DeviceBrandProper = row[14] + '_' + str(randomNumber)
                    # DeviceBrandProper = str(row[14] '·' get_random_string(length=5))
                    # print(DeviceBrandProper)
                    # print(len(row))
                    # if row[21] is not None and row[21] != '':
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
                        messages.error(request, 'Device email address is missing, please fill in the email address and try again.')
                        return redirect('Dashboard')
                    
                    if row[4] == '' or row[5] == '':
                        messages.error(request, "Device user's firstname or last name is missing. Please complete and try again")
                        return redirect('Dashboard')                    

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
                        CompanyUniqueCode = request.user.email
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
                        CompanyUniqueCode = request.user.email
                        # CompanyUniqueCode = request.user.last_name
                    )
                    try:
                        # checkUniqueUser = User.objects.filter(username = row[17])
                        checkUniqueUser =  User.objects.create_user(
                        username = row[17], email = 'Staff Member', password =  StaffUniqueId, first_name = request.user.email, last_name = row[4] +' '+row[5]
                        )
                    except:
                         messages.error(request, 'Sorry, a staff with an email address you are trying to upload has already been uploaded.')
                         return redirect('DeviceInventory')
                    checkUniqueUser.save()
                else:
                    messages.error(request, 'Device List Updated Unsuccessfully')
                    return redirect('DeviceInventory')
            obj.save()
            form.save()
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

    # allUploadedDevices = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = request.user.email)
    allUploadedDevices = DeviceRegisterUpload.objects.filter(user = request.user)
    AllStaffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.email)
    # AllStaffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.last_name)
    workingSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(user = request.user))
    workingSystems = workingSystems1.count()
    badSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Faulty') & Q(user = request.user))
    badSystems = badSystems1.count()
    allUploadedDevicesCount = allUploadedDevices.count()
    numberOfDevicesPerPage = str(DeviceCountPerPage.objects.filter(user = request.user).first())
    allProfileImages = UserProfileImage.objects.all().first
    allSignUps = SignupForm.objects.all()
    context = {'AllStaffMembers':AllStaffMembers, 'allSignUps':allSignUps, 'allProfileImages':allProfileImages, 'allUploadedDevices':allUploadedDevices, 'numberOfDevicesPerPage':numberOfDevicesPerPage, 'allUploadedDevicesCount':allUploadedDevicesCount, 'workingSystems':workingSystems, 'badSystems':badSystems}
    return render(request, 'userarea/deviceinventory.html', context)


# SAVE DEVICE ONTO DATA BASE FROM FORM FUNTIONALITY STARTS HERE
def SaveDevice(request):
    # if request.method == 'POST' and 'deviceusedepartment' in request.POST:
    # deviceusedepartment = request.POST['deviceusedepartment']
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
    if request.method == 'POST' and 'MaintainStatus' in request.POST:
        MaintainStatus = request.POST['MaintainStatus']
        MaintainDeviceType = request.POST['MaintainDeviceType']
        MaintainType = request.POST['MaintainType']
        MaintainRequestDescription = request.POST['MaintainRequestDescription']
        MaintainDeviceName = request.POST['MaintainDeviceName']
        MaintainDeviceID = request.POST['MaintainDeviceID']
        MaintainDeviceIP = request.POST['MaintainDeviceIP']
        MaintainDeviceMAC = request.POST['MaintainDeviceMAC']
        MaintainDeviceCategory = request.POST['MaintainDeviceCategory']
        MaintainDeviceLocation = request.POST['MaintainDeviceLocation']
        MaintainDeviceUserFirstname = request.POST['MaintainDeviceUserFirstname']
        MaintainDeviceUserLastname = request.POST['MaintainDeviceUserLastname']
        MaintainRequesterEmailAddress = request.POST['MaintainRequesterEmailAddress']
        MaintainDeviceUserDepartment = request.POST['MaintainDeviceUserDepartment']
        MaintainRequester = request.POST['MaintainRequester']
        CompanyUniqueCode = request.POST['CompanyUniqueCode']
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
        

        form = MaintenanceRequest.objects.create(user = request.user, CompanyUniqueCode = CompanyUniqueCode, MaintainRequesterEmailAddress = MaintainRequesterEmailAddress, MaintainDeviceName = MaintainDeviceName, MaintainDeviceID = MaintainDeviceID, 
        MaintainDeviceIP = MaintainDeviceIP, MaintainType = MaintainType, MaintainDeviceMAC_ID = MaintainDeviceMAC, MaintainDeviceType = MaintainDeviceType, MaintainDeviceUserFirstname = MaintainDeviceUserFirstname,
        MaintainDeviceUserLastname = MaintainDeviceUserLastname, MaintainDeviceCategory = MaintainDeviceCategory, MaintainDeviceLocation = MaintainDeviceLocation, MaintainStatus = MaintainStatus,
        currentMonth = month1, MaintainRequester = MaintainRequester, MaintainDeviceUserDepartment = MaintainDeviceUserDepartment, MaintainRequestID = MaintainRequestID, MaintainRequestDescription = MaintainRequestDescription)

        form.save()
        return redirect('Maintainance')
    currentDeviceList = DeviceRegisterUpload.objects.get(Q(deviceid = name)  & Q(user = request.user))
    context = {'name':name, 'currentDeviceList':currentDeviceList}
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
def EditDevice(request, deviceid):
    MainDeviceData = DeviceRegisterUpload.objects.get(deviceid=deviceid)
    form = DeviceRegisterForm(request.POST or None, instance = MainDeviceData)
    if request.POST and form.is_valid():
        form.save()
        if form.save():
            messages.success(request, 'Device data saved successfully')
            return redirect('DeviceInventory')
        else:
            messages.success(request, 'Error saving device data')
    AllStaffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.email)
    context = {'AllStaffMembers':AllStaffMembers, 'form':form, 'id': id, 'MainDeviceData':MainDeviceData}
    return render(request, 'userarea/editdevice.html', context)


@login_required(login_url='Login')
def StaffMembers(request):
    randomNumberForStaff = random.randint(1000, 99999)
    StaffUniqueId = 'Staff-' + request.user.username + str(randomNumberForStaff)
    if request.method == 'POST' and 'staff_firstname' in request.POST:
        StaffID = StaffUniqueId
        staff_firstname = request.POST['staff_firstname']
        staff_lastname = request.POST['staff_lastname']
        staff_email = request.POST['staff_email']
        staff_role = request.POST['staff_role']
        staff_phonenumber = request.POST['staff_phonenumber']
        staff_location = request.POST['staff_location']
        CompanyUniqueCode = request.POST['CompanyUniqueCode']
        user = request.user

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
            username = staff_email, email = request.user.username, password =  StaffUniqueId, first_name = request.user.last_name, last_name = staff_firstname + staff_lastname)
            # username = staff_email, email = 'Staff Member', password =  StaffUniqueId, first_name = request.user.last_name, last_name = staff_firstname + staff_lastname)

            CreateStaff = StaffDataSet(StaffID=StaffID, staff_firstname=staff_firstname, staff_lastname=staff_lastname, 
            staff_email=staff_email, staff_role=staff_role, staff_phonenumber=staff_phonenumber, user=user,
            staff_location=staff_location, CompanyUniqueCode=CompanyUniqueCode)

            checkUniqueUser.save()
            CreateStaff.save()
            messages.success(request, 'Staff created successfully')
            return redirect('StaffMembers')
        


        # CreateStaff = StaffDataSet(StaffID=StaffID, staff_firstname=staff_firstname, staff_lastname=staff_lastname, 
        # staff_email=staff_email, staff_role=staff_role, staff_phonenumber=staff_phonenumber, user=user,
        # staff_location=staff_location, CompanyUniqueCode=CompanyUniqueCode)
        
        # CREATE USER ACCOUNT FOR STAFF FUNCTIIONALITY STARTS HERE

        # try:
        #     print(staff_email)
        #     checkUniqueUserMain = User.objects.get(username = staff_email)
        #     if checkUniqueUserMain is None:
        #         print('checkUniqueUserMain')
        #         checkUniqueUser =  User.objects.create_user(
        #         username = staff_email, email = 'Staff Member', password =  StaffUniqueId, first_name = request.user.last_name, last_name = row[4] +' '+row[5])
        #         checkUniqueUser.save()
        #         CreateStaff.save()
        # except:
        #     messages.error(request, 'Sorry, a staff with an email address you are trying to upload has already been uploaded.')
        #     return redirect('StaffMembers')
        # # CREATE USER ACCOUNT FOR STAFF FUNCTIIONALITY ENDS HERE


        # try:
        #     # CreateStaff.save()
        #     # messages.error(request, 'Staff created successfully')
        #     return redirect('StaffMembers')
        # except:
        #     messages.error(request, 'Staff was not created, try again')
        #     return redirect('StaffMembers')

    staffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.email)
    allDevices = DeviceRegisterUpload.objects.all()
    allUploadedDevices = DeviceRegisterUpload.objects.all()
    staffCount = staffMembers.count()
    allSignUps = SignupForm.objects.all()
    AllUsers = User.objects.all()
    context = {'AllUsers':AllUsers, 'allDevices':allDevices, 'allSignUps':allSignUps, 'staffMembers': staffMembers, 'staffCount':staffCount, 'allUploadedDevices':allUploadedDevices}
    return render(request, 'userarea/staffpage.html', context)


@login_required(login_url='Login')
def StaffDetails(request, id):
    allStaff = StaffDataSet.objects.get(id = id)
    if request.method == 'POST' and 'deviceusedepartment' in request.POST and 'deviceToAssign' not in request.POST:
        uniqueId = 'Device-' + get_random_string(length=5)
        if request.POST['devicebrand']:
            randomNumber = random.randint(100, 9999)
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
        CompanyUniqueCode = request.POST['CompanyUniqueCode']
        user = request.user

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


    # allUploadedDevices = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = request.user.email)
    allUploadedDevices = DeviceRegisterUpload.objects.filter(user = request.user)
    allUploadedDevicesNotAssigned = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.email) & Q(staffUserID = 'None'))
    # allUploadedDevicesNotAssigned = DeviceRegisterUpload.objects.filter(Q(CompanyUniqueCode = request.user.last_name) & Q(staffUserID = 'None'))
    allSignUps = SignupForm.objects.all()
    context = {'allSignUps':allSignUps, 'allStaff' : allStaff, 'allUploadedDevices' : allUploadedDevices, 'allUploadedDevicesNotAssigned':allUploadedDevicesNotAssigned}
    return render(request, 'userarea/staffdetails.html', context)


# @login_required(login_url='Login')
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
    context = {'allProfileImages':allProfileImages, 'allSignUps':allSignUps, 'form' : form, 'currentUser' : currentUser}
    return render(request, 'userarea/editprofile.html', context)


def ProfilePage(request, pk):
    requestUser = SignupForm.objects.get(id = pk)
    allSignUps = SignupForm.objects.all()
    allUsers = User.objects.all()
    context = {'allSignUps':allSignUps, 'allUsers':allUsers, 'requestUser':requestUser}
    return render(request, 'userarea/profilepage.html', context)


@login_required(login_url='Login')
def Dashboard(request):
    if request.method == "POST" and 'csv_file' in request.FILES:
        username = request.POST['username']
        savetimedata = request.POST['savetimedata']
        filedata = request.FILES.get('csv_file', False)
        
        print(str(username))
        print(str(filedata))
        if 'csv' not in str(filedata):
            messages.success(request, 'Wrong File Format. Please Use The Recommended CSV File.')
            return redirect('Dashboard')

        if request.FILES.get('csv_file') is None:
            messages.success(request, 'Device List Updated Failed! Please Select A File.')
            return redirect('Dashboard')
        
        if not request.POST['username']:
            messages.success(request, 'Device List Updated Failed! User Name Missing Login Again.')
            return redirect('Dashboard')

        form = uploadedDeviceData.objects.create(username = username, mainfile = filedata)
        form.save()
        obj = uploadedDeviceData.objects.all().first()
        randomNumber = random.randint(100, 9999)

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
                    # DeviceBrandProper = row[14]+'_'+str(randomNumber)
                    randomNumberForStaff = random.randint(1000, 99999)
                    StaffUniqueId = 'Staff-' + request.user.username + str(randomNumberForStaff)
                    # DeviceBrandProper = row[14] + '·' + str(randomNumber)
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
                        messages.error(request, 'Device email address is missing, please fill in the email address and try again.')
                        return redirect('Dashboard')
                    
                    if row[4] == '' or row[5] == '':
                        messages.error(request, "Device user's firstname or last name is missing. Please complete and try again")
                        return redirect('Dashboard')


                    AllStaffCheck = StaffDataSet.objects.filter(staff_email = row[17])
                    print('----------------------------------------------------------------')
                    print(AllStaffCheck)
                    if AllStaffCheck:
                        print('email already exists')
                        messages.error(request, 'Sorry, a staff with an email address you are trying to upload has already been uploaded.')
                        return redirect('Dashboard')
                   

                    # AllStaffCheck = StaffDataSet.objects.filter(staff_email = row[17])
                    # print(AllStaffCheck)
                    # if AllStaffCheck:
                    #     print('email already exists')
                    #     messages.error(request, 'Sorry, a staff with an email address you are trying to upload has already been uploaded.')
                    #     return redirect('Dashboard')
                        

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
                        CompanyUniqueCode = request.user.email
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
                        CompanyUniqueCode = request.user.email
                    )
                    
                    try:
                        checkUniqueUser =  User.objects.create_user(
                        username = row[17], email = 'Staff Member', password =  StaffUniqueId, first_name = request.user.email, last_name = row[4] +' '+row[5]
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
        CompanyUniqueCode = request.POST['CompanyUniqueCode']
        user = request.user

        if not request.POST['deviceusedepartment']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Department.")
            return redirect('Dashboard')
        
        if not request.POST['devicemacaddress']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's MAC Address.")
            return redirect('Dashboard')
        
        if not request.POST['devicetype']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Type.")
            return redirect('Dashboard')
            

        if not request.POST['devicelocation']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Location.")
            return redirect('Dashboard')
        
        if not request.POST['devicestatus']:
            messages.error(request, "Device uploaded failed. Please Indicate This Device's Working Condition.")
            return redirect('Dashboard')

        if staffUserID:
            AllStaffMembers = StaffDataSet.objects.get(StaffID = staffUserID).staff_email
            print(AllStaffMembers)
            deviceuseremail = AllStaffMembers

        
        SaveDeviceProper = DeviceRegisterUpload.objects.create(
            deviceusedepartment=deviceusedepartment, devicetype=devicetype, devicebrand=DeviceBrandProper, 
            deviceos=deviceos, devicecostofpurchase=devicecostofpurchase, devicename=devicename,
            devicemacaddress=devicemacaddress, devicelocation=devicelocation, deviceip=deviceip,
            devicestatus=devicestatus, staffUserID=staffUserID, CompanyUniqueCode=CompanyUniqueCode,
            deviceyearofpurchase=deviceyearofpurchase, user=user, devicedepreciationrate=depreciateRateReal,
            deviceid=uniqueId, deviceuseremail = deviceuseremail
        )

        try:
            SaveDeviceProper.save()
            messages.success(request, 'Device uploaded successfully')
            return redirect('Dashboard')
        except:
            messages.error(request, 'Device uploaded failed. Please Try again.')
            redirect('Dashboard')

        

    # allUploadedDevices = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = request.user.email)
    allUploadedDevices = DeviceRegisterUpload.objects.filter(user = request.user)
    # allUploadedDevices = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = request.user.last_name)
    allUploadedDevicesCount = allUploadedDevices.count()
    AllStaffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.email)
    # AllStaffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = request.user.last_name)
    StaffCount = AllStaffMembers.count()
    DeviceRegister1 = DeviceRegisterUpload.objects.filter(user=request.user)
    badSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Faulty') & Q(user = request.user))
    badSystems = badSystems1.count()
    workingSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(user = request.user))
    workingSystems = workingSystems1.count()
    warningSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Critical') & Q(user = request.user))
    warningSystems = warningSystems1.count()
    labels = ['Healthy Devices', 'Faulty Devices', 'Critical Devices']
    data = [workingSystems, badSystems, warningSystems]
    thisYear = datetime.today().year
    allSignUps = SignupForm.objects.filter(Q(email = request.user.email) & Q(companyUniqueID = request.user.email)).first
    allUsers = User.objects.all()
    allSignupsForUpdatePopup = SignupForm.objects.filter(email = request.user.email)
    context = {'allSignupsForUpdatePopup':allSignupsForUpdatePopup, 'AllStaffMembers':AllStaffMembers,'allUsers':allUsers, 'allSignUps':allSignUps, 'labels':labels,'thisYear':thisYear, 'data':data, 'allUploadedDevices':allUploadedDevices,'badSystems':badSystems, 'allUploadedDevicesCount':allUploadedDevicesCount, 'StaffCount':StaffCount}
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
    writer.writerow(['Device IP Address', 'Device Name', 'Device MAC Address', 'Device Network Adapter Company',
     'Device User First Name', 'Device User Last Name', 'Device Status', 'Company Name', 'Device Use Department', 
     'Device Port Number', 'Device Multiple Packet', 'Device Index', 'Device Type',
     'Device Location', 'Device Brand', 'Device Operating System', 'Device Cost Of Purchase','Device User Email Address', 
     'Device User Phone Number', 'Device User Job Resumption Date', 'Device Working Status', 'Device Year Of Purchase'
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
       Q( Q(deviceid__icontains = q) | 
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

        form = uploadedDeviceData.objects.create(username = username, mainfile = filedata)
        form.save()
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
                        messages.error(request, 'Device email address is missing, please fill in the email address and try again.')
                        return redirect('Dashboard')
                    
                    if row[4] == '' or row[5] == '':
                        messages.error(request, "Device user's firstname or last name is missing. Please complete and try again")
                        return redirect('Dashboard')

                    

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
                        CompanyUniqueCode = request.user.email
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
                        CompanyUniqueCode = request.user.email
                        # CompanyUniqueCode = request.user.last_name
                    )
                    try:
                        checkUniqueUser =  User.objects.create_user(
                        username = row[17], email = 'Staff Member', password =  StaffUniqueId, first_name = request.user.email, last_name = row[4] +' '+row[5]
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
    deviceToDelete.delete()
    messages.success(request, 'Device Successfully Deleted!')
    return redirect('DeviceInventory')
    messages.success(request, 'Device Successfully Deleted!')
    return render(request, 'userarea/deviceinventory.html')


def AllDeviceDelete(request):
    AllDevices = DeviceRegisterUpload.objects.filter(user = request.user)
    messages.error(request, 'All devices have been deleted successfully!')
    AllDevices.delete()
    return redirect('DeviceInventory')



def DeleteStaff(request, pk):
    staffToDelete = StaffDataSet.objects.get(id=pk)
    staffToDelete.delete()
    messages.success(request, 'Staff Details Successfully Deleted!')
    return redirect('StaffMembers')
    messages.success(request, 'Device Successfully Deleted!')
    return render(request, 'userarea/deviceinventory.html')



def EditProfileImg(request):
    if request.method == 'POST' and profilepicture in request.POST:
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



def AllInstalledSoftwares(request):
    item = winapps.list_installed
    allSignUps = SignupForm.objects.all()
    context = {'item':item, 'allSignUps':allSignUps}
    return render(request, 'userarea/allinstalledapp.html', context)

# Franklin-franklin.i@itservicedeskafrica.com
def UpdateCompanyDetails(request, email, name):
    WorkingUsers = User.objects.get(Q(email=email) & Q(username=name))
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
