# from site import USER_BASE
from django.urls import reverse
from django.contrib import messages
# from django.http import HttpResponse
# from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
import csv
from django.db.models import Q
from useronboard.models import SignupForm, UserProfileImage
from datetime import datetime
from django.utils.crypto import get_random_string
import json
from django.contrib.auth.models import User
from datetime import date

# import datetime; 

# Create your views here.


@login_required(login_url='Login')
def NavBar(request):
    allSignUps = SignupForm.objects.all()
    allProfileImages = UserProfileImage.objects.all().first
    context = {'allProfileImages':allProfileImages, 'allSignUps': allSignUps}
    return render(request, 'general.html', context)


@login_required(login_url='Login')
def Reports(request):
    allProfileImages = UserProfileImage.objects.all().first
    allUsers = User.objects.all()
    allSignUps = SignupForm.objects.all()
    context = {'allSignUps':allSignUps, 'allUsers':allUsers, 'allProfileImages':allProfileImages}
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
    #  & Q(user = request.user)
    allMaintains = MaintenanceRequest.objects.filter(user = request.user)
    allMaintainsCount = allMaintains.count()
    numberOfDevicesPerPage = DeviceCountPerPage.objects.filter(user = request.user).first()
    allProfileImages = UserProfileImage.objects.all().first
    allUsers = User.objects.all()
    allSignUps = SignupForm.objects.all()
    context = {'allSignUps':allSignUps, 'allUsers':allUsers, 'allProfileImages':allProfileImages, 'allMaintains':allMaintains, 'allMaintainsCount':allMaintainsCount, 'numberOfDevicesPerPage':numberOfDevicesPerPage}
    return render(request, 'userarea/maintainance.html', context)


@login_required(login_url='Login')
def Settings(request):
    allProfileImages = UserProfileImage.objects.all().first
    allUsers = User.objects.all()
    allSignUps = SignupForm.objects.all()
    context = {'allSignUps':allSignUps, 'allUsers':allUsers, 'allProfileImages':allProfileImages}
    return render(request, 'userarea/settings.html', context)


@login_required(login_url='Login')
def DeviceInventory(request):
    if request.method == 'POST' and 'savedevicefromform' in request.POST:
        print('This File Is Coming From -The Save device form')
        user = request.user
        devicetype = request.POST['devicetype']
        devicebrand = request.POST['devicename']
        devicemacaddress = request.POST['devicemacaddress']
        deviceuser = request.POST['deviceuser']
        deviceip = request.POST['deviceip']
        devicestatus = request.POST['devicestatus']
        devicelocation = request.POST['devicelocation']
        deviceid = 'Device-' + get_random_string(length=5)

        if not request.POST['devicename']:
            messages.error(request, 'Please give this device a name.')
            return redirect('DeviceInventory')
        
        if not request.POST['devicetype']:
            messages.error(request, 'You did not select a device type.')
            return redirect('DeviceInventory')

        form = DeviceRegisterUpload(user=request.user, devicebrand=devicebrand, devicetype=devicetype, deviceip=deviceip, devicestatus=devicestatus,
        devicemacaddress=devicemacaddress, deviceuser=deviceuser, devicelocation=devicelocation, deviceid=deviceid)

        form.save()
        redirect('DeviceInventory')

    # CSV UPLOAD STARTS HERE
    if request.method == "POST" and 'csv_file' in request.FILES:
        username = request.POST['username']
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

        with open(obj.mainfile.path, 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    pass
                elif len(row) < 9:
                    messages.success(request, 'Upload Failed: Please Use The Sample CSV File Provided')
                    return redirect('Dashboard')
                elif len(row) > 9:
                    today = date.today()

                    dateForWeekNumber = datetime.today()
                    weekNumber = dateForWeekNumber.isocalendar().week
                    uniqueId = 'Device-' + get_random_string(length=5)
                    # print(len(row))
                    if row[20]:
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
                        savetimedata = today.strftime("%B %d, %Y"),
                        weekNumberSaved = weekNumber
                    ),
                    StaffDataSet.objects.create(
                        user = request.user,
                        deviceuserfirstname = row[4],
                        deviceuserlastname = row[5],
                        deviceuserphonenumber = row[18],
                        devicelocation = row[13],
                        deviceuseremail = row[17],
                        staffDevice = uniqueId,
                        staffrole = row[8],
                        staffDeviceName = row[1],
                        staffDeviceStatus = row[6]
                    )
                else:
                    messages.error(request, 'Device List Updated Unsuccessfully')
                    return redirect('DeviceInventory')
            obj.save()
        messages.success(request, 'Device List Updated Successfully')
        return redirect('DeviceInventory')
    # CSV UPLOAD ENDS HERE

    # PAGINATION COUNT FORM STARTS HERE
    if request.method == 'POST'  and 'numofitemsperpage' in request.POST:
        count = request.POST['numofitemsperpage']
        form = DeviceCountPerPage(user = request.user, count = count)
        form.save()
        messages.success(request, 'Device display per page count saved successfully')
        return redirect('DeviceInventory')
    # PAGINATION COUNT FORM ENDS HERE
    
    # DEVICE DELETE FUNCTIONALITY STARTS HERE
    if request.method == 'POST' and 'requestFrom' in request.POST:
        print('deleteChoice gotten')
        deleteChoice = request.POST['deleteChoice']
        DeletedDevices.objects.create()
        print(deleteChoice)
        userData = request.POST['requestFrom']
        deviceSearch = DeviceRegisterUpload.objects.filter(id = deleteChoice)
        if deviceSearch is None:
            messages.success(request, 'Device delete failed: Device not found!')
            return redirect('DeviceInventory')
        
    # DEVICE DELETE FUNCTIONALITY ENDS HERE

    allUploadedDevices = DeviceRegisterUpload.objects.filter(user = request.user)
    workingSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(user = request.user))
    workingSystems = workingSystems1.count()
    badSystems1 = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Faulty') & Q(user = request.user))
    badSystems = badSystems1.count()
    allUploadedDevicesCount = allUploadedDevices.count()
    numberOfDevicesPerPage = DeviceCountPerPage.objects.filter(user = request.user).first()
    allProfileImages = UserProfileImage.objects.all().first
    allSignUps = SignupForm.objects.all()
    context = {'allSignUps':allSignUps, 'allProfileImages':allProfileImages, 'allUploadedDevices':allUploadedDevices, 'numberOfDevicesPerPage':numberOfDevicesPerPage, 'allUploadedDevicesCount':allUploadedDevicesCount, 'workingSystems':workingSystems, 'badSystems':badSystems}
    return render(request, 'userarea/deviceinventory.html', context)


@login_required(login_url='Login')
def StaffMembers(request):
    staffMembers = StaffDataSet.objects.filter(user = request.user)
    allUploadedDevices = DeviceRegisterUpload.objects.all()
    # allUploadedDevices = DeviceRegisterUpload.objects.filter(user = request.user)
    staffCount = staffMembers.count()
    allProfileImages = UserProfileImage.objects.all().first
    allSignUps = SignupForm.objects.all()
    context = {'allSignUps':allSignUps, 'allProfileImages':allProfileImages, 'staffMembers': staffMembers, 'staffCount':staffCount, 'allUploadedDevices':allUploadedDevices}
    return render(request, 'userarea/staffpage.html', context)


@login_required(login_url='Login')
def StaffDetails(request, id):
    allStaff = StaffDataSet.objects.get(id = id)
    allUploadedDevices = DeviceRegisterUpload.objects.all()
    allProfileImages = UserProfileImage.objects.all().first
    allSignUps = SignupForm.objects.all()
    context = {'allSignUps':allSignUps, 'allProfileImages':allProfileImages, 'allStaff' : allStaff, 'allUploadedDevices' : allUploadedDevices}
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




    # form = UserRegistrationForm(request.POST or None, instance = currentUser)
    # UserformUpdate = UpdateUserForm(request.POST or None, instance = request.user)
    # # if request.POST and form.is_valid() and request.FILES:
    # # if request.POST and form.is_valid() and UserformUpdate.is_valid():
    # print('valid!')
    # if form.is_valid() and UserformUpdate.is_valid():
    #     print('valid passed!')
    #     userRegForm = form.save()
    #     userForm = UserformUpdate.save(False)
    #     userForm = userRegForm
    #     userForm.save()
    #     # if form.save() and UserformUpdate.save():
    #     if userRegForm.save() and userForm.save():

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

        with open(obj.mainfile.path, 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    pass
                elif len(row) < 9:
                    messages.success(request, 'Upload Failed: Please Use The Sample CSV File Provided')
                    return redirect('Dashboard')
                elif len(row) > 9:
                    # print(len(row))
                    today = date.today()
                                        
                    dateForWeekNumber = datetime.today()
                    weekNumber = dateForWeekNumber.isocalendar().week
                    uniqueId = 'Device-' + get_random_string(length=5)
                    if row[20]:
                        depreciateRate = 2023 - int(row[21])
                    else:
                        depreciateRate = '0%'
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
                        savetimedata = today.strftime("%B %d, %Y"),
                        # savetimedata = today.strftime("%b-%d-%Y")
                        weekNumberSaved = weekNumber
                    ),
                    StaffDataSet.objects.create(
                        user = request.user,
                        deviceuserfirstname = row[4],
                        deviceuserlastname = row[5],
                        deviceuserphonenumber = row[18],
                        devicelocation = row[13],
                        deviceuseremail = row[17],
                        staffDevice = uniqueId,
                        staffrole = row[8],
                        staffDeviceName = row[1],
                        staffDeviceStatus = row[6]
                        # deviceuserdateofresumption = row[17]
                    )
                else:
                    messages.error(request, 'Device List Updated Unsuccessfully')
                    return redirect('Dashboard')
            obj.save()
        messages.success(request, 'Device List Updated Successfully')
        return redirect('Dashboard')



    if request.method == 'POST' and 'savedevicefromform' in request.POST:
        print('This File Is Coming From -The Save device form')
        user = request.user
        devicetype = request.POST['devicetype']
        devicebrand = request.POST['devicename']
        devicemacaddress = request.POST['devicemacaddress']
        deviceuser = request.POST['deviceuser']
        deviceip = request.POST['deviceip']
        devicestatus = request.POST['devicestatus']
        savetimedata = request.POST['savetimedata']
        devicelocation = request.POST['devicelocation']
        deviceid = 'Device-' + get_random_string(length=5)

        if not request.POST['devicename']:
            messages.error(request, 'Please give this device a name.')
            return redirect('Dashboard')
        
        if not request.POST['devicetype']:
            messages.error(request, 'You did not select a device type.')
            return redirect('Dashboard')

        form = DeviceRegisterUpload(user=request.user, devicebrand=devicebrand, devicetype=devicetype, deviceip=deviceip, devicestatus=devicestatus,
        devicemacaddress=devicemacaddress, savetimedata=savetimedata, deviceuser=deviceuser, devicelocation=devicelocation, deviceid=deviceid)

        form.save()
        redirect('Dashboard')

    allUploadedDevices = DeviceRegisterUpload.objects.filter(user = request.user)
    allUploadedDevicesCount = allUploadedDevices.count()
    staffMembers = StaffDataSet.objects.filter(user = request.user)
    StaffCount = staffMembers.count()
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
    allSignUps = SignupForm.objects.all()
    allUsers = User.objects.all()
    allProfileImages = UserProfileImage.objects.all().first
    context = {'allProfileImages':allProfileImages, 'allUsers':allUsers, 'allSignUps':allSignUps, 'labels':labels,'thisYear':thisYear, 'data':data, 'allUploadedDevices':allUploadedDevices,'badSystems':badSystems, 'allUploadedDevicesCount':allUploadedDevicesCount, 'StaffCount':StaffCount}
    return render(request, 'userarea/dashboard.html', context)


# @login_required(login_url='Login')
def EditDeviceData(request, deviceip):
    deviceData = DeviceRegisterUpload.objects.get(deviceip=deviceip)
    form = DeviceRegisterForm(request.POST or None, instance = deviceData)
    if request.POST and form.is_valid():
        form.save()
    context = {'form':form, 'id': id}
    return render(request, 'userarea/editDeviceData.html', context)



# MAIN DEVICE EDIT DATA PAGE LINKED BELOW
def EditDevice(request, deviceid):
    MainDeviceData = DeviceRegisterUpload.objects.get(deviceid=deviceid)
    form = DeviceRegisterForm(request.POST or None, instance = MainDeviceData)
    if request.POST and form.is_valid():
        form.save()
        if form.save():
            messages.success(request, 'Device data saved successfully')
        else:
            messages.success(request, 'Error saving device data')
    context = {'form':form, 'id': id, 'MainDeviceData':MainDeviceData}
    return render(request, 'userarea/editdevice.html', context)


# EDIT STAFF DETAILS STARTS BELOW
def EditStaff(request, staffid):
    currentStaff = StaffDataSet.objects.get(id = staffid)
    form = staffForm(request.POST or None, instance = currentStaff)
    if request.POST and form.is_valid():
        form.save()
        if form.save():
            messages.success(request, 'Staff details edited successfully')
        else:
            messages.success(request, 'Error saving staff details')
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
    return render(request, 'userarea/scannetwork.html')


# FULL SAMPLE CSV FILE
def downloadSampleFile(request):
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename =  Device Upload Sample File.csv'
    writer = csv.writer(response)
    writer.writerow(['Device IP Address', 'Device Name', 'Device MAC Address', 'Device Network Adapter Company',
     'Device User Full Name', 'Device Status', 'Company Name', 'Device Use Department', 
     'Device Port Number', 'Device Multiple Packet', 'Device Index', 'Device Type',
     'Device Location', 'Device Brand', 'Device Operating System', 'Device Cost Of Purchase','Device User Email Address', 
     'Device User Phone Number', 'Device User Job Resumption Date', 'Device Working Status', 'Device Year Of Purchase'
     ])
    writer.writerow(['20.20.0.27', 'DESKTOP-7687TC8', '20-10-7A-4E-9F-46', 'Gemtek Technology Co., Ltd.', 'John Doe', 'on', 
    'IT Service Desk Africa', 'IT Department', '433', 'Nil', '1', 'Laptop', 'Aba Abia State', 'Toshiba', 
    'Windows 10 Pro', 'N100, 000', 'johndoe@itservicedeskafrica.com', '0701 156 7240', '2020', 'Good', '2023'])
    return response



# SAMPLE LIST TO SEE HOW HEADERS ARE ON CSV FILE
def downloadSampleCSVHeaders(request):
    response = HttpResponse('')
    response['Content-Disposition'] = 'attachment; filename = CSV Sample File.csv'
    writer = csv.writer(response)
    writer.writerow(['Device IP Address', 'Device Name', 'Device MAC Address', 'Device Network Adapter Company',
     'Device User Full Name', 'Device Status', 'Company Name', 'Device Use Department', 
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
    allProfileImages = UserProfileImage.objects.all().first
    context = {'allProfileImages':allProfileImages, 'allUsers':allUsers, 'allSignUps': allSignUps}
    return render(request, 'userarea/updateimage.html', context)