from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# from useronboard.models import SignupForm
from django.contrib import messages
# from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .tokens import account_activation_token

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


# from django_ratelimit.decorators import ratelimit
# from django.utils.decorators import method_decorator

# Create your views here.

def NavBar(request):
    return render(request, 'generalonboard.html')


def PreSignUpPage(request):
    return render(request, 'useronboard/presignuppage2.html')


def Home(request):
    return render(request, 'useronboard/home.html')


    
# @method_decorator(ratelimit(key='user_or_ip', rate='5/m'))
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
        else:
            form = SignupForm(user=request.user, companyname=companyname, companyUniqueID=companyUniqueID, email=email, phone=phonenumber, password=password, repassword=rtpassword)
            user = User.objects.create_user(username=companyname, email=email, password=password, first_name=phonenumber, last_name=companyUniqueID)
            form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            user.save(False)
            # try:
            #     activateEmail(request, user, email)
            # except:
            #     print('Registration mail was not sent successfully')
            return redirect('Dashboard')

            # return redirect('Login')
    return render(request, 'useronboard/signup.html')


# @method_decorator(ratelimit(key='user_or_ip', rate='5/m'))
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
        LoginStatus.objects.create(user = user, email = companymail, status = 'Online')

        if user is not None:
            try:
                # notifyLoginEmail(request, user, companymail)
                login(request, user)
                return redirect('Dashboard')
            except:
                messages.error(request, 'Login Failed: Please Try Again.')
                return redirect('Login')

        else:
            # print(error)
            messages.error(request, 'Login Failed: Please Try Again!!')
            return render(request, 'useronboard/login.html')
    return render(request, 'useronboard/login.html')



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
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'https' if request.is_secure() else 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'info@itservicedeskafrica.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					except:
						redirect("password/password_reset.html")
						messages.error(request, 'An error occoured. Please contact ITSA Support.')
					return redirect ("password_reset/done/")
			else:
				redirect("password/password_reset.html")
				messages.error(request, 'Email address is not registered as an admin. Please contact your company IT Support admin to provide your password.')

	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})


# RESET PASSWORD VIEW ENDS HERE


# SEND EMAIL AFTER REGISTRATION
def activateEmail(request, user, to_email):
    mail_subject = "Your Company registered on the Device Health Management System[DHMS] Platform with ITSA."
    recipient_list = [to_email, ]
    message = render_to_string("mailouts/account_verification_email.html", {
        'user': user.email,
        'domain': get_current_site(request).domain if request.is_secure() else 'http://127.0.0.1:8000/',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = send_mail(mail_subject, message, 'dhmsinventoryapp@gmail.com', recipient_list)
    if email:
        # messages.success(request, 'A confimation email was sent to your inb')
        print('Sent a confirmation email')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly')



def notifyLoginEmail(request, user, to_email):
    mail_subject = "Someone logged into your DHMS account."
    recipient_list = [to_email, ]
    message = render_to_string("mailouts/account_login_email.html", {
        'user': user.email,
        # 'domain': 'http://127.0.0.1:8000/',
        'domain': get_current_site(request).domain if request.is_secure() else 'http://127.0.0.1:8000/',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = send_mail(mail_subject, message, 'dhmsinventoryapp@gmail.com', recipient_list)
    if email:
        print('Email sent')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly')


