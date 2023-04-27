from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# from useronboard.models import SignupForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import *

# Create your views here.

def NavBar(request):
    return render(request, 'generalonboard.html')


def PreSignUpPage(request):
    return render(request, 'useronboard/presignuppage2.html')


    
def SignUpPage(request):
    if request.method == 'POST':
    # if request.method == 'POST' and request.FILES:
        companyname = request.POST['companyname']
        email = request.POST['companymail']
        phonenumber = request.POST['phonenumber']
        # address = request.POST['address']
        password = request.POST['password']
        rtpassword = request.POST['rtpassword']
        # address = request.POST['address']
        # numberofdevices = request.POST['numofdevices']
        # website = request.POST['website']
        # Profilepicture = request.FILES.get('profilepic', False)
        
        
        if not request.POST['companyname']:
            messages.success(request, 'Registration Failed: Enter Your Company Name')
            return redirect('SignUpPage')
            messages.success(request, 'Registration Failed: Enter Your Company Name')

        if not request.POST['companymail']:
            messages.success(request, 'Registration Failed: Enter Your Company Email Address')
            return redirect('SignUpPage')
            messages.success(request, 'Registration Failed: Enter Your Company Email Address')
        
        if not request.POST['phonenumber']:
            messages.success(request, 'Registration Failed: Enter Your Company Phone Number')
            return redirect('SignUpPage')
            messages.success(request, 'Registration Failed: Enter Your Company Phone Number')


        if (password != rtpassword):
            messages.error(request, 'Passwords Do Not Match!')
            return redirect('SignUpPage')
            messages.error(request, 'Passwords Do Not Match!')

        data = SignupForm.objects.filter(companyname=companyname)
        UserData = User.objects.filter(username=companyname)
        if data or UserData:
            messages.error(request, 'Sorry, Company Name Is Already Taken, Please Use Another Company Name')
            return redirect('SignUpPage')
            messages.error(request, 'Sorry, Company Name Is Already Taken')

        else:
            messages.success(request, 'Registration Successful')
            form = SignupForm(companyname=companyname, email=email, phone=phonenumber, password=password, repassword=rtpassword)

            user = User.objects.create_user(
                username=companyname, email=email, password=password, first_name=phonenumber, last_name=phonenumber)

            UserProfileImgDetailsUpdate = UserProfileImage.objects.create(userReg = companyname)
        
            form.save()
            login(request, user)
            form.save()
            user.save()
            UserProfileImgDetailsUpdate.save()

            return redirect('Login')
    return render(request, 'useronboard/signup.html')


def Login(request):
    if request.method == 'POST':
        companymail = request.POST['companymail']
        password = request.POST['password']
        try:
            user = User.objects.get(email=companymail)
            if user:
                userEmail = user.email
                print(user.email)
        except:
            messages.error(request, 'Login Failed: Please Try Again.')
            return redirect('Login')
        
        user = authenticate(request, username=user, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfull')
            return redirect('Dashboard')

        else:
            # print(error)
            messages.error(request, 'Login Failed: Please Try Again!!')
            return render(request, 'useronboard/login.html')
    return render(request, 'useronboard/login.html')



# # EDIT USER SIGNUP DETAILS STARTS BELOW
# def EditUserSignupDetails(request, id):
#     currentUser = SignupForm.objects.get(id = id)
#     form = UserRegistrationForm(request.POST or None, instance = currentUser)
#     if request.POST and form.is_valid() and request.FILES:
#         form.save()
#         if form.save():
#             messages.success(request, 'Your Company details have been updated successfully')
#         else:
#             messages.success(request, 'Error saving company details')
#     context = {'form' : form, 'currentUser' : currentUser}
#     return render(request, 'userarea/editprofile.html', context)