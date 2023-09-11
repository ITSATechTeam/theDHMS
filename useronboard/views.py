from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# from useronboard.models import SignupForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import *

# RESET PASSWORD IMPORTS STARTS HERE
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# RESET PASSWORD IMPORTS ENDS HERE

# Create your views here.

def NavBar(request):
    return render(request, 'generalonboard.html')


def PreSignUpPage(request):
    return render(request, 'useronboard/presignuppage2.html')


def Home(request):
    return render(request, 'useronboard/home.html')


    
def SignUpPage(request):
    if request.method == 'POST':
    # if request.method == 'POST' and request.FILES:
        companyname = request.POST['companyname']
        email = request.POST['companymail']
        phonenumber = request.POST['phonenumber']
        companyUniqueID = companyname + '-' + email
        # address = request.POST['address']
        password = request.POST['password']
        rtpassword = request.POST['rtpassword']
        
        
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
                username=companyname, email=email, password=password, first_name=phonenumber, last_name=companyUniqueID)

            UserProfileImgDetailsUpdate = UserProfileImage.objects.create(userReg = companyname)
        
            form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.save()
            user.save(False)
            # serProfileImgDetailsUpdate = UserProfileImage.objects.create(user = user.username, userReg = companyname)
            # user.save()
            UserProfileImgDetailsUpdate.save()

            return redirect('Dashboard')
    return render(request, 'useronboard/signup.html')


def Login(request):
    if request.method == 'POST':
        companymail = request.POST['companymail']
        password = request.POST['password']
        try:
            user = User.objects.get(email=companymail)
            if user:
                userEmail = user.email
                # print(user.email)
        except:
            messages.error(request, 'Login Failed: Please Try Again.')
            return redirect('Login')
        
        user = authenticate(request, username=user, password=password)

        if user is not None:
            login(request, user)
            # messages.success(request, 'Login Successfull')
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



# RESET PASSWORD VIEW STARTS HERE
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "DHMS Inventory Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'itservicedeskafrica.com',
					'site_name': 'dhms@itservicedeskafrica.com',
					# "uid": urlsafe_base64_encode(force_bytes(user.pk)).decode(),
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					except:
						redirect("password/password_reset.html")
						messages.error(request, 'An error occoured. Please contact ITSA Support.')
					# return redirect ("password_reset_done")
					return redirect ("password_reset/done/")
			else:
				redirect("password/password_reset.html")
				messages.error(request, 'Email address is not registered as an admin. Please contact your company IT Support admin to provide your password.')

	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})


# RESET PASSWORD VIEW ENDS HERE