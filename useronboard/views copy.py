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
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

# RESET PASSWORD IMPORTS STARTS HERE
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
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
    
    
def csrf_failure(request, reason=""):
    return render(request, 'useronboard/403_csrf.html')



    
# @method_decorator(ratelimit(key='user_or_ip', rate='5/m'))
def SignUpPage(request):
    if request.method == 'POST':
        companyname = request.POST['companyname']
        email = request.POST['companymail']
        phonenumber = request.POST['phonenumber']
        companyUniqueID = (companyname+'-'+email).replace(" ", "")
        # address = request.POST['address']
        password = request.POST['password']
        # rtpassword = request.POST['rtpassword']
        phoneNumberReview = str(phonenumber)
        
        
        if not request.POST['companyname']:
            messages.success(request, 'Registration Failed: Enter Your Company Name')
            return redirect('SignUpPage')

        if not request.POST['companymail']:
            messages.success(request, 'Registration Failed: Enter Your Company Email Address')
            return redirect('SignUpPage')
        
        if not request.POST['phonenumber']:
            messages.success(request, 'Registration Failed: Enter Your Company Phone Number')
            return redirect('SignUpPage')


        if (int(phonenumber) < 10):
            messages.error(request, 'Your phone number is invalid!')
            return redirect('SignUpPage')
        
        
        if (len(phoneNumberReview) < 10):
            messages.error(request, 'Your phone number is invalid!')
            return redirect('SignUpPage')
        
        
        
        if (len(phoneNumberReview) > 17):
            messages.error(request, 'Your phone number is invalid!')
            return redirect('SignUpPage')
            

        data = SignupForm.objects.filter(companyname=companyname)
        UserData = User.objects.filter(username=companyname)
        UserDataCheckEmail = User.objects.filter(email=email)
        if data or UserData:
            messages.error(request, 'Sorry, Company Name Is Already Taken, Please Use Another Company Name')
            return redirect('SignUpPage')

        elif UserDataCheckEmail:
            messages.error(request, 'Sorry, Email Address Is Already Taken, Please Use A Unique Email Address')
            return redirect('SignUpPage')
            
        else:
            form = SignupForm(companyname=companyname, companyUniqueID=companyUniqueID, email=email, phone=phonenumber, password=password)
            user = User.objects.create_user(username=companyname, email=email, password=password, first_name=phonenumber, last_name=companyUniqueID)
            form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            user.save(False)
            activateEmail(request, user, email, companyname)
            try:
                activateEmail(request, user, email)
            except:
                print('Registration mail was not sent successfully')
            return redirect('Dashboard')

            # return redirect('Login')
    return render(request, 'useronboard/signup.html')


# @method_decorator(ratelimit(key='user_or_ip', rate='5/m'))
def Login(request):
    next = ""
    if request.GET:  
        next = request.GET['next']
        
    if request.method == 'POST':
        companymail = request.POST['companymail']
        password = request.POST['password']
        try:
            user = User.objects.get(email=companymail)
            if user:
                pass
            else:
                messages.error(request, 'An error occured, please try again.')
                return redirect('Login') 
                
            isacompany = SignupForm.objects.get(email = companymail)
            if isacompany:
                 pass
            else:
                messages.error(request, 'You are not allowed to use an Administrator account at this time, kindly contact support.')
                return redirect('Login') 
        except:
            messages.error(request, 'The email address you entered is not registered. Please create an account to continue.')
            return redirect('SignUpPage')
        
        user = authenticate(request, username=user, password=password)
        # LoginStatus.objects.create(user = user, email = companymail, status = 'Online')

        if user is not None:
            login(request, user)
            try:
                myCompanyName = User.objects.filter(email = companymail).values_list('username', flat=True).first()
                notifyLoginEmail(request, user, companymail, myCompanyName)
            except:
                print('error sending login notification email to user')
            if next == "":
                return redirect('Dashboard')
            else:
                return HttpResponseRedirect(next)
                
            return redirect('Dashboard')

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
def activateEmail(request, user, to_email, companyname):
    recipient_list = [to_email, ] 

    context = {'companyname':companyname}
    html_message = render_to_string("mailouts/account_verification_email.html", context=context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject = "Your Company registered on the Device Health Management System[DHMS].", 
        body = plain_message,
        from_email = 'dhmsinventoryapp@gmail.com',
        to= recipient_list
        )

    message.attach_alternative(html_message, "text/html")
    message.send()

    if message:
        print('Sent a login notification email')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly')




def notifyLoginEmail(request, user, to_email, myCompanyName):
    recipient_list = [to_email, ]

    context = {'myCompanyName':myCompanyName}
    html_message = render_to_string("mailouts/account_login_email.html", context=context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject = "Your DHMS Account Has Been Accessed.", 
        body = plain_message,
        from_email = 'dhmsinventoryapp@gmail.com',
        to= recipient_list
        )

    message.attach_alternative(html_message, "text/html")
    message.send()

    if message:
        print('Sent a login notification email')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly')


# def sync_user_relations(us
