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
from useronboard.models import LoginStatus, SignupForm
# 
from django.conf import settings

ms_identity_web = settings.MS_IDENTITY_WEB

# Create your views here.

from datetime import datetime, timedelta
delta = 1
time_now = datetime.now()
time_ago = time_now - timedelta(minutes=delta)
# print(time_now.hour)
# print(time_ago.hour)
if time_now.hour == 24 :
    allLoginStatusMain = LoginStatus.objects.all()
    allLoginStatusMain.delete()


# @login_required(login_url='Login')
def StaffNavBar(request):
    return render(request, 'staffgeneral.html')


@login_required(login_url='StaffLogin')
# @ms_identity_web.login_required
def StaffDashboard(request):
    JanMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'Jan')).count()
    FebMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'Feb')).count()
    MarchMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'Mar')).count()
    AprilMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'Apr')).count()
    MayMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'May')).count()
    JuneMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'June')).count()
    JuneMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'Jun')).count()
    JulyMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'Jul')).count()
    AugMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'August')).count()
    SeptMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'Sep')).count()
    OctMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'Oct')).count()
    NovMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'Nov')).count()
    DecMaintainReqs = MaintenanceRequest.objects.filter(Q(MaintainDeviceUserID = request.user.email) & Q(currentMonth = 'Dec')).count()
    
    MaintenanceRequests = MaintenanceRequest.objects.filter(MaintainDeviceUserID = request.user.last_name)
    AllStaffMembers = StaffDataSet.objects.all()
    MaintenanceRequestsCount = MaintenanceRequest.objects.filter(MaintainRequesterEmailAddress = request.user.username).count()
    MaintenanceRequestsPendingCount = MaintenanceRequest.objects.filter(Q(MaintainRequesterEmailAddress = request.user.username) & Q(MaintainStatus = 'Ongoing')).count()
    RegisteredDevices = DeviceRegisterUpload.objects.filter(staffUserID = request.user.email)
    RegisteredDevicesCount = DeviceRegisterUpload.objects.filter(staffUserID = request.user.email).count()
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
                # print(user.username)
        except:
            messages.error(request, 'Login Failed: Please Try Again .')
            return redirect('StaffLogin')
        
        user = authenticate(request, username=user, password=staffphonenumber)
        LoginStatus.objects.create(user = user, email = staffemail, status = 'Online')

        if user is not None:
            login(request, user)
            return redirect('StaffDashboard')

        else:
            # print(error)
            messages.error(request, 'Login Failed: Please Try Again or Contact Your IT Admin.')
            return redirect('StaffLogin')
    return render(request, 'staffapp/stafflogin.html')



# from datetime import timedelta
# AUTO_LOGOUT = {'SESSION_TIME': timedelta(minutes=1)}


def StaffLogout(request):
    MainLoginStatus = LoginStatus.objects.filter(email = request.user.username)
    MainLoginStatus.delete()
    logout(request)
    messages.success(request, 'Logout Successful')
    return redirect('StaffLogin')

# @ms_identity_web.login_required
@login_required(login_url='StaffLogin')
def StaffDeviceInventory(request):
    MaintenanceRequests = MaintenanceRequest.objects.filter(MaintainRequesterEmailAddress = request.user.username).count()
    RegisteredDevices = DeviceRegisterUpload.objects.filter(staffUserID = request.user.email)
    RegisteredDevicesFaulty = DeviceRegisterUpload.objects.filter(Q(staffUserID = request.user.email) & Q(devicestatus = 'Faulty')).count()
    RegisteredDevicesWorking = DeviceRegisterUpload.objects.filter(Q(staffUserID = request.user.email) & Q(devicestatus = 'Working')).count()
    RegisteredDevicesCount = DeviceRegisterUpload.objects.filter(staffUserID = request.user.email).count()
    context = {'RegisteredDevicesWorking':RegisteredDevicesWorking,'MaintenanceRequests':MaintenanceRequests, 'RegisteredDevicesFaulty':RegisteredDevicesFaulty, 'RegisteredDevices':RegisteredDevices, 'RegisteredDevicesCount':RegisteredDevicesCount}
    return render(request, 'staffapp/staffdeviceinventory.html', context)


# @ms_identity_web.login_required
def StaffSupport(request):
    return render(request, 'staffapp/staffsupport.html')


# VIEW DEVICE DETAILS PAGE
# @ms_identity_web.login_required
@login_required(login_url='StaffLogin')
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
        MaintainDeviceUserID = request.POST['MaintainDeviceUserID']
        # MaintainDeviceUserFullName = request.POST['MaintainDeviceUserFullName']
        MaintainRequesterEmailAddress = request.POST['MaintainRequesterEmailAddress']
        MaintainRequester = request.POST['MaintainRequester']
        MaintainDeviceUserDepartment = request.POST['MaintainDeviceUserDepartment']
        MaintainDeviceType = request.POST['MaintainDeviceType']
        CompanyUniqueCode = request.POST['CompanyUniqueCode']
        # currentMonth = request.POST['currentMonthName']
        MaintainRequestID = 'maintain' + '_' + str(randomNumber)

        dateNow = datetime.now()
        month1 = dateNow.strftime("%b")
        # print("Current Month Full Name:", month1)
        # print("dateNow", dateNow)

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
        MaintainDeviceIP = MaintainDeviceIP, MaintainDeviceMAC_ID = MaintainDeviceMAC, MaintainType = MaintainType, MaintainDeviceUserID = MaintainDeviceUserID, MaintainDeviceUserDepartment = MaintainDeviceUserDepartment,
        MaintainDeviceCategory = MaintainDeviceCategory, MaintainDeviceLocation = MaintainDeviceLocation, MaintainStatus = MaintainStatus,
        currentMonth = month1, MaintainDeviceType = MaintainDeviceType, MaintainRequester = MaintainRequester, MaintainRequestID = MaintainRequestID, MaintainRequestDescription = MaintainRequestDescription)

        form.save()
        return redirect('StaffMaintainance')
    # AllMaintenanceRequest = MaintenanceRequest.objects.filter(MaintainDeviceID = name)
    AllMaintenanceRequest = MaintenanceRequest.objects.filter(MaintainDeviceName = name)
    # print(type(AllMaintenanceRequest))
    # print(type(name))
    # AllMaintenanceRequestCount = MaintenanceRequest.objects.filter(MaintainDeviceID = name).count()
    AllMaintenanceRequestCount = MaintenanceRequest.objects.filter(MaintainDeviceName = name).count()
    AllDevices = DeviceRegisterUpload.objects.all()
    currentDeviceList = DeviceRegisterUpload.objects.get(deviceid = name)
    # currentDeviceList = DeviceRegisterUpload.objects.get(Q(devicebrand = name)  & Q(user = request.user))
    context = {'AllDevices':AllDevices, 'name':name, 'currentDeviceList':currentDeviceList, 'AllMaintenanceRequest' : AllMaintenanceRequest, 'AllMaintenanceRequestCount' : AllMaintenanceRequestCount}
    return render(request, 'staffapp/staffdevicedetails.html', context)




# @login_required(login_url='Login')
# @ms_identity_web.login_required
def StaffSearchresult(request):
    # print('seaching...')
    if request.GET.get('q') == 'AllStatus':
        deviceSearch = DeviceRegisterUpload.objects.filter(
            Q(devicestatus__icontains = 'Working') |
            Q(deviceuserfirstname__icontains = 'Critical') |
            Q(deviceuserfirstname__icontains = 'Faulty') )
            
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if request.method == 'GET':
        # print(q)
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
        # print("Current Month Full Name:", month1)
        # print("dateNow", dateNow)
        # print("today", today)
        date = datetime.today()
        weekNumber = date.isocalendar().week
        # print('this week number:', weekNumber)
        allUsers = User.objects.all()
    
    context = {'allUsers':allUsers, 'deviceSearch': deviceSearch, 'deviceSearchCount':deviceSearchCount}
    return render(request, 'staffapp/staffsearchresult.html', context)



# MAINTENANCE REQUEST PAGE FOR STARTS HERE
@login_required(login_url='StaffLogin')
# @ms_identity_web.login_required
def StaffMaintainance(request):
    # REDIRECT TO VIEW DETAILS PAGE FOR SELECTED MAINTENANCE REQUEST
    if request.method == 'GET' and 'requesttoviewdetails' in request.GET:
        requesttoviewdetailsMain = request.GET['requesttoviewdetails']
        # print(' see requesttoviewdetailsMain below:')
        # print(requesttoviewdetailsMain)
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


# @ms_identity_web.login_required
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
    currentDeviceMain = str(MaintenanceRequest.objects.get(MaintainRequestID = name).MaintainDeviceID)
    currentDeviceDetails = DeviceRegisterUpload.objects.get(deviceid = currentDeviceMain).staffUserID
    currentDeviceUser = StaffDataSet.objects.get(StaffID = currentDeviceDetails)
    # print(currentDeviceUser)
    AllCommments = AddedMaintenanceComments.objects.all()
    AllMaintainDevice = MaintenanceRequest.objects.get(MaintainRequestID = name)
    context = {'currentDeviceUser':currentDeviceUser, 'currentDeviceDetails':currentDeviceDetails, 'AllCommments':AllCommments, 'AllMaintainDevice':AllMaintainDevice, 'currentDevice':currentDevice}
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


def StaffDeleteAddedComment(request, pk, name):
    commentToDelete = AddedMaintenanceComments.objects.get(id = pk)
    commentToDelete.delete()
    messages.error(request, 'Comment has been deleted')
    # return response
    return redirect('StaffMaintainanceDetails', name = name)

def AzureSignin(request):
    return render(request, 'auth/sign_in_status.html')

    
def AuthRedirect(request):
    return render(request, 'staffapp/staffdashboard2.html')

# input time in seconds
# t = input("Enter the time in seconds: ")
  
# # function call
# countdown(request)

@ms_identity_web.login_required
def index(request):
    AllCompanies = SignupForm.objects.all()
    thisStaffName = request.identity_context_data.username
    Allstaffmembers = StaffDataSet.objects.all().values_list('staff_firstname', flat=True)
    for a in Allstaffmembers:
        # print(thisStaffName)
        if a == thisStaffName:
            existingUserName = a
            # print(existingUserName)
            # IF USER EXIST ALREADY, LOG USER IN
            currentStaffUser = StaffDataSet.objects.filter(staff_firstname = existingUserName).values_list('staff_email', flat=True).first()
            currentStaffUserID = StaffDataSet.objects.filter(staff_firstname = existingUserName).values_list('StaffID', flat=True).first()
            currentStaffUserMain = User.objects.filter(username = currentStaffUser)
            user = authenticate(request, username=currentStaffUser, password=currentStaffUserID)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('StaffDashboard')
        # # LoginStatus.objects.create(user = user, email = youremailaddress, status = 'Online')

        # if user is not None:
        #     login(request, user)
        #     return redirect('StaffDashboard')
        
        else:
            existingUserName = 'NoUser'


    findStaffFromDB = list(StaffDataSet.objects.filter(staff_firstname = thisStaffName).values_list('staff_firstname', flat=True))
    if request.method == 'POST' and 'companyname' in request.POST:
        companyname = request.POST['companyname']
        yourphonenumber = request.POST['yourphonenumber']
        staff_firstname = request.POST['staff_firstname']
        yourofficelocation = request.POST['yourofficelocation']
        youremailaddress = request.POST['youremailaddress']
        staff_role = request.POST['staff_role']

        if not request.POST['companyname']:
            messages.error(request, 'Kindly select the company you work with.')
            return redirect('index')
       
        if not request.POST['yourphonenumber']:
            messages.error(request, 'Kindly insert your company phone number.')
            return redirect('index')
       
        if not request.POST['youremailaddress']:
            messages.error(request, 'Kindly insert your company email address.')
            return redirect('index')
       
        if not request.POST['yourofficelocation']:
            messages.error(request, 'Kindly insert your office location.')
            return redirect('index')
       
        if not request.POST['staff_firstname']:
            messages.error(request, "You didn't enter a full name, Please do.")
            return redirect('index')
       
        if not request.POST['staff_role']:
            messages.error(request, "Kindly enter your role of department you work with.")
            return redirect('index')

        randomNumberForStaff = random.randint(1000, 99999)
        try:
            SelectedCompany = list(SignupForm.objects.filter(email = companyname).values_list('companyname', flat=True))[0]
            SelectedCompanyUniqueID = list(SignupForm.objects.filter(email = companyname).values_list('companyUniqueID', flat=True))[0]
            StaffUniqueId = 'Staff-' + SelectedCompany + str(randomNumberForStaff)
        except:
            messages.error(request, "An error occured. Kindly fill the form completely")
            return redirect('index')


        checkIfUsernameExit = User.objects.filter(username = youremailaddress)
        checkIfPhoneNumberExit = StaffDataSet.objects.filter(staff_phonenumber = yourphonenumber)
        checkIfStaffEmailExit = StaffDataSet.objects.filter(staff_email = youremailaddress)

        if checkIfStaffEmailExit: 
            messages.error(request, 'Registration Failed: The email address you entered is in use already.')
            return redirect('StaffDashboard')

        elif checkIfPhoneNumberExit:
            messages.error(request, 'Registration Failed: The Phone Number you entered is in use already.')
            return redirect('StaffDashboard')

        else:
            try:            
                StaffDataSetForm = StaffDataSet(staff_firstname = staff_firstname, staff_phonenumber = yourphonenumber, 
                staff_email = youremailaddress, staff_location = yourofficelocation, staff_role = staff_role, StaffID = StaffUniqueId, 
                CompanyUniqueCode = SelectedCompanyUniqueID)
    
                checkUniqueUser =  User.objects.create_user(username = youremailaddress, email = StaffUniqueId, password =  StaffUniqueId, 
                last_name = staff_firstname, first_name = SelectedCompanyUniqueID)
                
                StaffDataSetForm.save()
                checkUniqueUser.save()
            except:
                messages.error(request, 'An error occured when creating your account. Please try again, and if this persists, kindly contact ITSA support')
                return redirect('StaffDashboard')
                
            
        
        user = authenticate(request, username=youremailaddress, password=StaffUniqueId)
        # LoginStatus.objects.create(user = user, email = youremailaddress, status = 'Online')

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('StaffDashboard')

        else:
            # print(error)
            messages.error(request, 'Login Failed: Please Try Again or Contact Your IT Admin.')
            return redirect('StaffLogin')
            return redirect('index')

    
    context = {'AllCompanies':AllCompanies, 'existingUserName':existingUserName, 'findStaffFromDB':findStaffFromDB}
    return render(request, 'staffapp/staffdashboard.html', context)




from django.conf import settings
ms_identity_web = settings.MS_IDENTITY_WEB

@ms_identity_web.login_required
def secret_page(request):
    return render(request, 'secret.html')

@ms_identity_web.login_required
def organizations(request):
    AllCompanies = SignupForm.objects.all()
    thisStaffName = request.identity_context_data.username
    Allstaffmembers = StaffDataSet.objects.all().values_list('staff_firstname', flat=True)
    for a in Allstaffmembers:
        # print(thisStaffName)
        if a == thisStaffName:
            existingUserName = a
            # IF USER EXIST ALREADY, LOG USER IN
            currentStaffUser = StaffDataSet.objects.filter(staff_firstname = existingUserName).values_list('staff_email', flat=True).first()
            currentStaffUserID = StaffDataSet.objects.filter(staff_firstname = existingUserName).values_list('StaffID', flat=True).first()
            currentStaffUserMain = User.objects.filter(username = currentStaffUser)
            user = authenticate(request, username=currentStaffUser, password=currentStaffUserID)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('StaffDashboard')
        
        else:
            existingUserName = 'NoUser'
            

    findStaffFromDB = list(StaffDataSet.objects.filter(staff_firstname = thisStaffName).values_list('staff_firstname', flat=True))
    if request.method == 'POST' and 'companyname' in request.POST:
        companyname = request.POST['companyname']
        yourphonenumber = request.POST['yourphonenumber']
        staff_firstname = request.POST['staff_firstname']
        yourofficelocation = request.POST['yourofficelocation']
        youremailaddress = request.POST['youremailaddress']
        staff_role = request.POST['staff_role']

        if not request.POST['companyname']:
            messages.error(request, 'Kindly select the company you work with.')
            return redirect('index')
       
        if not request.POST['yourphonenumber']:
            messages.error(request, 'Kindly insert your company phone number.')
            return redirect('index')
       
        if not request.POST['youremailaddress']:
            messages.error(request, 'Kindly insert your company email address.')
            return redirect('index')
       
        if not request.POST['yourofficelocation']:
            messages.error(request, 'Kindly insert your office location.')
            return redirect('index')
       
        if not request.POST['staff_firstname']:
            messages.error(request, "You didn't enter a full name, Please do.")
            return redirect('index')
       
        if not request.POST['staff_role']:
            messages.error(request, "Kindly enter your role of department you work with.")
            return redirect('index')

        randomNumberForStaff = random.randint(1000, 99999)
        try:
            SelectedCompany = list(SignupForm.objects.filter(email = companyname).values_list('companyname', flat=True))[0]
            SelectedCompanyUniqueID = list(SignupForm.objects.filter(email = companyname).values_list('companyUniqueID', flat=True))[0]
            print(SelectedCompanyUniqueID)
            StaffUniqueId = 'Staff-' + SelectedCompany + str(randomNumberForStaff)
        except:
            messages.error(request, "An error occured. Kindly fill the form completely")
            return redirect('index')


        checkIfUsernameExit = User.objects.filter(username = youremailaddress)
        checkIfPhoneNumberExit = StaffDataSet.objects.filter(staff_phonenumber = yourphonenumber)
        checkIfStaffEmailExit = StaffDataSet.objects.filter(staff_email = youremailaddress)

        if checkIfStaffEmailExit: 
            messages.error(request, 'Registration Failed: The email address you entered is in use already.')
            return redirect('StaffDashboard')

        elif checkIfPhoneNumberExit:
            messages.error(request, 'Registration Failed: The Phone Number you entered is in use already.')
            return redirect('StaffDashboard')

        else:
            try:            
                StaffDataSetForm = StaffDataSet(staff_firstname = staff_firstname, staff_phonenumber = yourphonenumber, 
                staff_email = youremailaddress, staff_location = yourofficelocation, staff_role = staff_role, StaffID = StaffUniqueId, 
                CompanyUniqueCode = SelectedCompanyUniqueID)
    
                checkUniqueUser =  User.objects.create_user(username = youremailaddress, email = StaffUniqueId, password =  StaffUniqueId, 
                last_name = staff_firstname, first_name = SelectedCompanyUniqueID)
                
                StaffDataSetForm.save()
                checkUniqueUser.save()
            except:
                messages.error(request, 'An error occured when creating your account. Please try again, and if this persists, kindly contact ITSA support')
                return redirect('StaffDashboard')
                
            
        
        user = authenticate(request, username=youremailaddress, password=StaffUniqueId)
        # LoginStatus.objects.create(user = user, email = youremailaddress, status = 'Online')

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('StaffDashboard')

        else:
            # print(error)
            messages.error(request, 'Login Failed: Please Try Again or Contact Your IT Admin.')
            return redirect('StaffLogin')
            return redirect('index')

    
    context = {'AllCompanies':AllCompanies, 'existingUserName':existingUserName, 'findStaffFromDB':findStaffFromDB}
    return render(request, 'staffapp/staffdashboard.html')
