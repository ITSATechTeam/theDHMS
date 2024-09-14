# from datetime import datetime, timedelta
import datetime
import re
from time import strftime
from django.utils import timezone
import random
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
from django.utils.crypto import get_random_string
from getstream import Stream
from getstream.models import UserRequest
from getstream.models import (
    CallRequest,
    MemberRequest,
)


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



def contains_other_characters(email):
    # Check if '@' is in the email
    if '@' in email:
        # Split the email into two parts
        local_part, domain_part = email.split('@', 1)
        
        # Check if either part contains other characters
        return (any(char.isalnum() or char in '_-+' for char in local_part) or
                any(char.isalnum() or char in '_-+' for char in domain_part))
    return False

    
    
# @method_decorator(ratelimit(key='user_or_ip', rate='5/m'))
def SignUpPage(request):
    try:          
        if request.method == 'POST':
            companyname = request.POST['companyname']
            email = request.POST['companymail']
            phonenumber = request.POST['phonenumber']
            companyUniqueID = (companyname+'-'+email).replace(" ", "")
            # address = request.POST['address']
            password = request.POST['password']
            # rtpassword = request.POST['rtpassword']
            
            
            # if contains_other_characters(email):
            #     messages.error(request, 'Invalid email address')
            #     return redirect('SignUpPage')
            
            
            if not request.POST['companyname']:
                messages.success(request, 'Registration Failed: Enter Your Company Name')
                return redirect('SignUpPage')
            
            # if len(phonenumber) > 14 :
            #     messages.success(request, 'Phone number can not be more than 14 digits')
            #     return redirect('SignUpPage')

            if not request.POST['companymail']:
                messages.success(request, 'Registration Failed: Enter Your Company Email Address')
                return redirect('SignUpPage')

            # if request.POST['companymail'].contain:
            #     messages.success(request, 'Registration Failed: Enter Your Company Email Address')
            #     return redirect('SignUpPage')
            
            if not request.POST['phonenumber']:
                messages.success(request, 'Registration Failed: Enter Your Company Phone Number')
                return redirect('SignUpPage')


            # if (password != rtpassword):
            #     messages.error(request, 'Passwords Do Not Match!')
            #     return redirect('SignUpPage')

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
                # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                user.save(False)
                # activateEmail(request, user, email, companyname)
                try:
                    activateEmail(request, user, email)
                except:
                    print('Registration mail was not sent successfully')
                messages.error(request, 'Regitration was successful. Kindly login to continue.')
                return redirect('Login')

                # return redirect('Login')
        return render(request, 'useronboard/signup.html')
    except:
        messages.error(request, 'An error occured. Kindly check your connectivity and try again.')
        return redirect('SignUpPage')


# @method_decorator(ratelimit(key='user_or_ip', rate='5/m'))
def Login(request):        
    if request.method == 'POST':
        companymail = request.POST['companymail']
        password = request.POST['password']
        try:
            user = User.objects.get(email=companymail)   
            print(user) 
        except:
            messages.error(request, 'No user with the email address was found on the DHMS.')
            return redirect('SignUpPage') 

        isacompany = SignupForm.objects.filter(email = companymail)
        if isacompany:
                pass
        else:
            messages.error(request, 'You are not allowed to use an Administrator account at this time, kindly contact support.')
            return redirect('Login')
        
        # Check for max OTP attempts
        try:
            # OTP SETUP CODE STARTS HERE        
            authUser = authenticate(request, username=user, password=password)
            if authUser is not None:
                if(AccountValidation.objects.filter(useremail=companymail)):
                    LatestAccountValidationEntry = AccountValidation.objects.filter(useremail=companymail).first()
                    userMaxOTPTry = LatestAccountValidationEntry.max_otp_try
                    userMaxOut = LatestAccountValidationEntry.otp_max_out
                    userOTPExpiry = LatestAccountValidationEntry.otp_expiry
                    
                    if int(userMaxOTPTry) <= 3 and userMaxOut is None:
                        otp = random.randint(1000, 9999)
                        userMaxOTPTryNew = int(userMaxOTPTry) -1
                        clientUserName = User.objects.get(email = companymail).username
                        otp_user_waittime = timezone.now() + datetime.timedelta(hours=1)
                        SendOTPForLogin(request, otp, companymail, clientUserName)
                        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
                        request.session['useremail'] = companymail
                        request.session['password'] = password
                        AccountValidationSave = AccountValidation.objects.create(useremail = companymail,otp = otp,  otp_expiry = otp_expiry, otp_max_out = otp_user_waittime,  max_otp_try = userMaxOTPTryNew)
                        AccountValidationSave.save()
                        return redirect('Verify_otp') 
                    
                    if int(userMaxOTPTry) == 1:
                        otp = random.randint(1000, 9999)
                        otp_user_waittime = timezone.now() + datetime.timedelta(hours=1)
                        print('otp_user_waittime')
                        print(otp_user_waittime)
                        userMaxOTPTryNew = int(userMaxOTPTry) -1
                        clientUserName = User.objects.get(email = companymail).username
                        SendOTPForLogin(request, otp, companymail, clientUserName)
                        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
                        request.session['useremail'] = companymail
                        request.session['password'] = password
                        AccountValidation.objects.create(useremail = companymail,otp = otp,  otp_expiry = otp_expiry, otp_max_out = otp_user_waittime, max_otp_try = userMaxOTPTryNew)
                        return redirect('Verify_otp') 

                    elif int(userMaxOTPTry) <= 0 and timezone.now() < userMaxOut:
                        
                    # FORMAT REMAINING TIME SECTION ENDS HERE

                        remainingTime = userMaxOut - timezone.now() 
                        duration = str(remainingTime)
                        dot_index = duration.find('.')
                        if dot_index != -1:
                            part_before_dot = duration[:dot_index]
                        else:
                            part_before_dot = duration
                        print(part_before_dot)

                        colon_index = part_before_dot.find(':')
                        if colon_index != -1:
                            part_after_colon = part_before_dot[colon_index + 1:]
                        else:
                            part_after_colon = part_before_dot 
                            
                        dot_index2 = part_after_colon.find(':')
                        if dot_index2 != -1:
                            FinalDuration = part_after_colon[:dot_index2]
                        else:
                            FinalDuration = part_after_colon
                    # FORMAT REMAINING TIME SECTION ENDS HERE                            
                        messages.error(request, f'Max OTP trial reached or OTP has expired, try to login again after about {FinalDuration} minutes')
                        return redirect('Login')
                    

                    elif int(userMaxOTPTry) >= 0 and timezone.now() > userOTPExpiry:
                        otp = random.randint(1000, 9999)
                        userMaxOTPTryNew = 3
                        clientUserName = User.objects.get(email = companymail).username
                        otp_user_waittime = None
                        # otp_user_waittime = timezone.now() + datetime.timedelta(hours=1)
                        SendOTPForLogin(request, otp, companymail, clientUserName)
                        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
                        request.session['useremail'] = companymail
                        request.session['password'] = password
                        AccountValidation.objects.create(useremail = companymail, otp = otp, otp_expiry = otp_expiry, otp_max_out = otp_user_waittime,  max_otp_try = userMaxOTPTryNew)
                        return redirect('Verify_otp')
                    
                    elif int(userMaxOTPTry) <= 0 and timezone.now() < userOTPExpiry:                    
                    # FORMAT REMAINING TIME SECTION ENDS HERE
                    
                        remainingTime = userMaxOut - timezone.now() 
                        duration = str(remainingTime)
                        dot_index = duration.find('.')
                        if dot_index != -1:
                            part_before_dot = duration[:dot_index] 
                        else:
                            part_before_dot = duration 
                        print(part_before_dot)

                        colon_index = part_before_dot.find(':')
                        if colon_index != -1:
                            part_after_colon = part_before_dot[colon_index + 1:]
                        else:
                            part_after_colon = part_before_dot 
                            
                        dot_index2 = part_after_colon.find(':')
                        if dot_index2 != -1:
                            FinalDuration = part_after_colon[:dot_index2]
                        else:
                            FinalDuration = part_after_colon

                    # FORMAT REMAINING TIME SECTION ENDS HERE
                        messages.error(request, f'Max OTP trial reached or OTP has expired, try to login again after about {FinalDuration} minutes')
                        return redirect('Login')  
                    
                    elif int(userMaxOTPTry) < 0 and timezone.now() > userOTPExpiry:
                        messages.error(request, f'OTP Expired, kindly login again to recieve a new OTP')
                        return redirect('Login')

                    else:
                        messages.error(request, f'An error occured')
                        return redirect('Login')  
                else:
                    otp = random.randint(1000, 9999)
                    otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
                    otp_user_waittime = None
                    # otp_user_waittime = timezone.now() + datetime.timedelta(hours=1)
                    max_otp_try = 3
                    AccountValidationSave = AccountValidation.objects.create(useremail = companymail, otp = otp, otp_expiry = otp_expiry, otp_max_out = otp_user_waittime, max_otp_try = max_otp_try)
                    AccountValidationSave.save()
                    clientUserName = User.objects.get(email = companymail).username
                    request.session['useremail'] = companymail
                    request.session['password'] = password
                    SendOTPForLogin(request, otp, companymail, clientUserName)
                    messages.success(request, f'Successfully generated OTP for {companymail}. Kindly check your email inbox for OTP')
                    return redirect('Verify_otp')        
                
            else:
                messages.error(request, 'Login details are incorrect.')
                return redirect('Login')
        except:
            messages.error(request, 'An error occured. Kindly check your connectivity and try again.')
            return redirect('Login')

        # OTP SETUP CODE ENDS HERE
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





def SendOTPForLogin(request, otp, to_email, clientUserName):
    recipient_list = [to_email, ]

    context = {'clientUserName':clientUserName, 'otp':otp, 'to_email':to_email}
    html_message = render_to_string("mailouts/login_otp_mail.html", context=context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject = "Your DHMS Login OTP.", 
        body = plain_message,
        from_email = 'dhmsinventoryapp@gmail.com',
        to= recipient_list
        )

    message.attach_alternative(html_message, "text/html")
    message.send()

    if message:
        print('Sent a OTP code via email')
    else:
        messages.error(request, f'Problem sending OTP code via email to {to_email}, check if you typed it correctly')



def Verify_otp(request):
    try:
        userEmailAddress = request.session['useremail']
        userEnteredPassword = request.session['password']
        if request.method == 'POST':
            otp = request.POST['otp']

            try:
                user = User.objects.get(email=userEmailAddress)
                if user:
                    pass
                else:
                    messages.error(request, 'An error occured, please try again.')
                    return redirect('login') 
                    
                isacompany = SignupForm.objects.get(email = userEmailAddress)
                if isacompany:
                    pass
                else:
                    messages.error(request, 'Sorry, you do not have an admin access. Kindly contact your company support for details')
                    return redirect('Login') 
            except:
                messages.error(request, 'Verification failed. Kindly try again or contact support for prompt assistance.')
                return redirect('Verify_otp')
            
            GetOTP = AccountValidation.objects.filter(useremail = userEmailAddress).first()
            if timezone.now() > GetOTP.otp_expiry:
                print(timezone.now())
                print(GetOTP.otp_expiry)
                messages.error(request, 'OTP Expired. Kindly Generate a New OTP')
                return redirect('Verify_otp')

            if otp == GetOTP.otp:
                user = authenticate(request, username=user, password=userEnteredPassword)
                if user is not None:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    AccountValidation.objects.filter(useremail = userEmailAddress).delete()
                    companyID = int(User.objects.filter(email = userEmailAddress).values_list('id', flat=True).first())
                    print('companyID')
                    print(type(companyID))
                    print(companyID)

                    # GetStream user creation starts here
                    client = Stream(api_key="8ssxqcb3y55c", api_secret="dgyyjjvm78eet9ny69abjwx6ewy858tnwmmyddyn7ufk978scj38bgsa7qte6rk9", timeout=3.0)
                    client.upsert_users(
                        UserRequest(
                            id=get_random_string(length=15), name=userEmailAddress, role="admin", custom={"country": "NG"}
                        ),
                    )
                    client.create_token(user_id=userEmailAddress, expiration=3600)
                    
                    # GetStream user creation ends here

                    try:
                        myCompanyName = User.objects.filter(email = userEmailAddress).values_list('username', flat=True).first()
                        notifyLoginEmail(request, user, userEmailAddress, myCompanyName)
                    except:
                        print('error sending login notification email to user')

                    return redirect('Dashboard')

                else:
                    # print(error)
                    messages.error(request, 'OTP Verification Failed.')
                    return redirect('Verify_otp')
            else:
                # print(error)
                messages.error(request, 'OTP Verification Failed.')
                return redirect('Verify_otp')
    except:
        messages.error(request, 'OTP Verification Failed. Kindly try again or contact support')
        return redirect('Login')


    context = {'useremail':userEmailAddress}
    return render(request, 'useronboard/otpverificationpage.html', context)


