from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from userarea.forms import EditMaintenanceRequest
from userarea.models import MaintenanceRequest, DeviceRegisterUpload, AddedMaintenanceComments, StaffDataSet
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import random
from datetime import datetime
from datetime import date

# Create your views here.


# @login_required(login_url='Login')
def StaffNavBar(request):
    return render(request, 'staffapp/staffgeneral.html')


@login_required(login_url='StaffLogin')
def StaffDashboard(request):
    JanMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'January')).count()
    FebMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'February')).count()
    MarchMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'March')).count()
    AprilMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'April')).count()
    MayMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'May')).count()
    JuneMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'June')).count()
    JuneMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'Jun')).count()
    JulyMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'July')).count()
    AugMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'August')).count()
    SeptMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'September')).count()
    OctMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'October')).count()
    NovMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'November')).count()
    DecMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(currentMonth = 'December')).count()
    
    MaintenanceRequests = MaintenanceRequest.objects.filter(MaintainRequesterEmailAddress = request.user.username)
    AllStaffMembers = StaffDataSet.objects.all()
    MaintenanceRequestsCount = MaintenanceRequest.objects.filter(MaintainRequesterEmailAddress = request.user.username).count()
    MaintenanceRequestsPendingCount = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(MaintainStatus = 'Ongoing')).count()
    RegisteredDevices = DeviceRegisterUpload.objects.filter(deviceuseremail = request.user.username)
    RegisteredDevicesCount = DeviceRegisterUpload.objects.filter(deviceuseremail = request.user.username).count()
    labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    data = [JanMaintainReqs, FebMaintainReqs, MarchMaintainReqs,
            AprilMaintainReqs, MayMaintainReqs, JuneMaintainReqs, 
            JulyMaintainReqs, AugMaintainReqs, SeptMaintainReqs,
            OctMaintainReqs, NovMaintainReqs, DecMaintainReqs]
    context = {'AllStaffMembers':AllStaffMembers, 'MaintenanceRequestsPendingCount':MaintenanceRequestsPendingCount, 'MaintenanceRequestsCount':MaintenanceRequestsCount, 'RegisteredDevicesCount':RegisteredDevicesCount, 'RegisteredDevices':RegisteredDevices, 'labels':labels, 'data':data, 'MayMaintainReqs':MayMaintainReqs, 'MaintenanceRequests':MaintenanceRequests}
    return render(request, 'staffapp/staffdashboard.html', context)


def StaffLogin(request):
    if request.method == 'POST':
        staffemail = request.POST['staffemailaddres']
        staffphonenumber = request.POST['staffphonenumber']
        try:
            user = User.objects.get(username=staffemail)
            if user:
                userEmail = user.email
                print(user.username)
        except:
            messages.error(request, 'Login Failed: Please Try Again .')
            return redirect('StaffLogin')
        
        user = authenticate(request, username=user, password=staffphonenumber)

        if user is not None:
            login(request, user)
            # messages.success(request, 'Login Successfull')
            return redirect('StaffDashboard')

        else:
            # print(error)
            messages.error(request, 'Login Failed: Please Try Again or Contact Your IT Admin.')
            return redirect('StaffLogin')

    return render(request, 'staffapp/stafflogin.html')


def StaffLogout(request):
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('StaffLogin')


def StaffDeviceInventory(request):
    MaintenanceRequests = MaintenanceRequest.objects.filter(MaintainRequesterEmailAddress = request.user.username).count()
    RegisteredDevices = DeviceRegisterUpload.objects.filter(deviceuseremail = request.user.username)
    RegisteredDevicesFaulty = DeviceRegisterUpload.objects.filter(Q(deviceuseremail = request.user.username) & Q(devicestatus = 'Faulty')).count()
    RegisteredDevicesWorking = DeviceRegisterUpload.objects.filter(Q(deviceuseremail = request.user.username) & Q(devicestatus = 'Working')).count()
    RegisteredDevicesCount = DeviceRegisterUpload.objects.filter(deviceuseremail = request.user.username).count()
    context = {'RegisteredDevicesWorking':RegisteredDevicesWorking,'MaintenanceRequests':MaintenanceRequests, 'RegisteredDevicesFaulty':RegisteredDevicesFaulty, 'RegisteredDevices':RegisteredDevices, 'RegisteredDevicesCount':RegisteredDevicesCount}
    return render(request, 'staffapp/staffdeviceinventory.html', context)


def StaffSupport(request):
    return render(request, 'staffapp/staffsupport.html')


# VIEW DEVICE DETAILS PAGE
def StaffViewDeviceDetails(request, name):
    randomNumber = random.randint(10, 9999)
    if request.method == 'POST' and 'MaintainStatus' in request.POST:
        MaintainStatus = request.POST['MaintainStatus']
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
        MaintainRequester = request.POST['MaintainRequester']
        MaintainDeviceUserDepartment = request.POST['MaintainDeviceUserDepartment']
        MaintainDeviceType = request.POST['MaintainDeviceType']
        CompanyUniqueCode = request.POST['CompanyUniqueCode']
        # currentMonth = request.POST['currentMonthName']
        MaintainRequestID = 'maintain' + '_' + str(randomNumber)

        dateNow = datetime.now()
        month1 = dateNow.strftime("%b")
        print("Current Month Full Name:", month1)
        print("dateNow", dateNow)

        if not request.POST['MaintainStatus']:
            messages.error(request, 'Kindly provide a maintenance status.')
            return redirect('StaffViewDeviceDetails', name=name)
        
        if not request.POST['MaintainType']:
            messages.success(request, 'Kindly provide a maintenance type.')
            return redirect('StaffViewDeviceDetails', name=name)
        
        if not request.POST['MaintainRequestDescription']:
            messages.success(request, 'Kindly provide a maintenance description.')
            return redirect('StaffViewDeviceDetails', name=name)
        

        # check if any request is already filed for this device
        

        form = MaintenanceRequest.objects.create(user = request.user, CompanyUniqueCode = CompanyUniqueCode, MaintainRequesterEmailAddress = MaintainRequesterEmailAddress, MaintainDeviceName = MaintainDeviceName, MaintainDeviceID = MaintainDeviceID, 
        MaintainDeviceIP = MaintainDeviceIP, MaintainDeviceMAC_ID = MaintainDeviceMAC, MaintainType = MaintainType, MaintainDeviceUserFirstname = MaintainDeviceUserFirstname, MaintainDeviceUserDepartment = MaintainDeviceUserDepartment,
        MaintainDeviceUserLastname = MaintainDeviceUserLastname, MaintainDeviceCategory = MaintainDeviceCategory, MaintainDeviceLocation = MaintainDeviceLocation, MaintainStatus = MaintainStatus,
        currentMonth = month1, MaintainDeviceType = MaintainDeviceType, MaintainRequester = MaintainRequester, MaintainRequestID = MaintainRequestID, MaintainRequestDescription = MaintainRequestDescription)

        form.save()
        return redirect('StaffMaintainance')
    AllMaintenanceRequest = MaintenanceRequest.objects.filter(MaintainDeviceName = name)
    print(type(AllMaintenanceRequest))
    print(type(name))
    AllMaintenanceRequestCount = MaintenanceRequest.objects.filter(MaintainDeviceName = name).count()
    AllDevices = DeviceRegisterUpload.objects.all()
    currentDeviceList = DeviceRegisterUpload.objects.get(devicebrand = name)
    # currentDeviceList = DeviceRegisterUpload.objects.get(Q(devicebrand = name)  & Q(user = request.user))
    context = {'AllDevices':AllDevices, 'name':name, 'currentDeviceList':currentDeviceList, 'AllMaintenanceRequest' : AllMaintenanceRequest, 'AllMaintenanceRequestCount' : AllMaintenanceRequestCount}
    return render(request, 'staffapp/staffdevicedetails.html', context)




# @login_required(login_url='Login')
def StaffSearchresult(request):
    print('seaching...')
    if request.GET.get('q') == 'AllStatus':
        deviceSearch = DeviceRegisterUpload.objects.filter(
            Q(devicestatus__icontains = 'Working') |
            Q(deviceuserfirstname__icontains = 'Critical') |
            Q(deviceuserfirstname__icontains = 'Faulty') )
            
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
    ) & Q(deviceuseremail = request.user.username))
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
    return render(request, 'staffapp/staffsearchresult.html', context)



# MAINTENANCE REQUEST PAGE FOR STARTS HERE
@login_required(login_url='StaffLogin')
def StaffMaintainance(request):
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



    allMaintains = MaintenanceRequest.objects.filter(user = request.user)
    allMaintainsCount = allMaintains.count()
    # numberOfDevicesPerPage = DeviceCountPerPage.objects.filter(user = request.user).first()
    allUsers = User.objects.all()
    allCompletedRequests = MaintenanceRequest.objects.filter(Q(MaintainStatus = 'Completed') & Q(user = request.user))
    allCompletedRequestsCount = allCompletedRequests.count()
    allCanceledRequests = MaintenanceRequest.objects.filter(Q(MaintainStatus = 'Canceled') & Q(user = request.user))
    allCanceledRequestsCount = allCanceledRequests.count()
    allOngoingRequests = MaintenanceRequest.objects.filter(Q(MaintainStatus = 'Ongoing') & Q(user = request.user))
    allOngoingRequestsCount = allOngoingRequests.count()
    context = {'allOngoingRequestsCount':allOngoingRequestsCount, 'allCompletedRequestsCount':allCompletedRequestsCount, 
    'allCanceledRequestsCount':allCanceledRequestsCount, 'allUsers':allUsers, 
    'allMaintains':allMaintains, 'allMaintainsCount':allMaintainsCount}
    return render(request, 'staffapp/staffmaintainance.html', context)



def StaffMaintainanceDetails(request, name):
    if request.method == 'POST' and 'addedComment' in request.POST:
        addedComentMain = request.POST['addedComment']
        if addedComentMain == '':
            return redirect('MaintainanceDetails', name = name)
        commenter = request.POST['commenter']
        CommentedMaintainDeviceName = request.POST['CommentedMaintainDeviceName']
        CommentedMaintainDeviceUser = request.POST['CommentedMaintainDeviceUser']
        CommentedMaintainRequester = request.POST['CommentedMaintainRequester']
        CommentedMaintainRequestID = request.POST['CommentedMaintainRequestID']
        commenterEmailAddress = request.POST['commenterEmailAddress']
        form = AddedMaintenanceComments.objects.create(
            commenter = commenter,
            commentProper = addedComentMain,
            CommentedMaintainDeviceName = CommentedMaintainDeviceName,
            CommentedMaintainDeviceUser = CommentedMaintainDeviceUser, 
            CommentedMaintainRequester = CommentedMaintainRequester,
            CommentedMaintainRequestID = CommentedMaintainRequestID,
            commenterEmailAddress = commenterEmailAddress
        )
        form.save()
# AllMaintainDevice
    currentDevice = str(MaintenanceRequest.objects.get(MaintainRequestID = name).MaintainRequestID)
    AllCommments = AddedMaintenanceComments.objects.all()
    AllMaintainDevice = MaintenanceRequest.objects.get(MaintainRequestID = name)
    context = {'AllCommments':AllCommments, 'AllMaintainDevice':AllMaintainDevice, 'currentDevice':currentDevice}
    return render(request, 'staffapp/staffmaintainrequestdetails.html', context)



def EditStaffMaintainanceDetails(request, name):
    selectedRequest = MaintenanceRequest.objects.get(MaintainRequestID = name)
    form = EditMaintenanceRequest(request.POST or None, instance = selectedRequest)
    if request.POST and form.is_valid():
        form.save()
        return redirect('StaffMaintainanceDetails', name = name)
    context = {'form':form, 'selectedRequest':selectedRequest}
    return render(request, 'staffapp/staffeditmaintenancereq.html', context)


def StaffSolution(request):
    return render(request, 'staffapp/staffsolution.html')


def StaffSetting(request):
    return render(request, 'staffapp/staffsetting.html')


