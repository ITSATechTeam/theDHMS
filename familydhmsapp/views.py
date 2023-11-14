from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import *
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

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
                user = authenticate(request, username=user, password=password)
            else:
                messages.error(request, 'The email address you entered is not registered. Please create an account to continue.')
                return redirect('UserReg')

        except:
            messages.error(request, 'The email address you entered is not registered. Please create an account to continue.')
            return redirect('UserReg')
        
        # user = authenticate(request, username=user, password=password)

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
    return render(request, 'familydhmsapp/familydashboard.html')


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


def FamilyMembers(request):
    return render(request, 'familydhmsapp/familymember.html')


def FamilyLogout(request):
    logout(request)
    messages.error(request, 'Logout Successfull.')
    return redirect('UserLogin')













