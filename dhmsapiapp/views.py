import os
from django.dispatch import receiver
from grpc import Status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from dhmsapiapp.activateuser import ActivateUserBeforeRegister
from .serializers import *
from useronboard.models import SignupForm
from userarea.models import *
# from useronboard.checkuserinfo import CheckUserData
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from studentdhms.models import Password_Reset
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
import random
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

# from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMessage


#   implement my customization of token claim when displaying user data I create a custome view for it as below:
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         token['email'] = user.email
#         # ...

#         return token
    
# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


# ORGANIZATION DHMS API STARTS HERE

# @api_view(['GET'])
# # @permission_classes((permissions.AllowAny,))
# @permission_classes([IsAuthenticated])
# def All_Organization(request):
#     AllUser = SignupForm.objects.all()
#     serializer = RegisterSerializer(AllUser, many=True)
#     return Response(serializer.data)


# import requests
@api_view(['POST', 'GET'])
def User_Login(request):
    # if request.method == 'GET':
        
    # RegisterSerializer
    if request.method == 'POST':   
        serializer = OrgLoginSerializer(data = request.data)
        # response = requests.get(request.path)
        # csrf_token = request.COOKIES['csrftoken']
        # headers = {'X-CSRFToken': csrf_token}
        
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            CheckUserAvaibility = SignupForm.objects.get(email = email)
            CheckUserModelAvaibility = User.objects.get(email = email)
            CheckUserUsername = User.objects.get(email = email).username
            if CheckUserAvaibility is None:
                return Response({
                    'status':400,
                    'message': 'Email and password do not match, Try again',
                    # 'error': serializer.error_messages
                })
            elif CheckUserModelAvaibility is None:
                return Response({
                    'status':400,
                    'message': 'User Email and password do not match, Try again',
                    'error': serializer.error_messages
                })
            else:
                user = authenticate(request, username=CheckUserUsername, password=password)
                token, created = Token.objects.get_or_create(user=user)
                # try:
                #     # token = Token.objects.create(user=user)
                #     token, created = Token.objects.get_or_create(user=user)

                # except Token.DoesNotExist:
                #     token = Token.objects.create(user=user)
                    
                # is_expired, token = token_expire_handler(token) # The implementation will be described further
                # user_serialized = UserSerializer(user)                  
                    
                if user is not None:
                    # print('login successful')
                    login(request, user)
                    # After successful login, retrieve the session ID
                    session_id = request.session.session_key
                    # print(session_id)
                    return Response({
                        'status':200,
                        'message': 'Login Successfull',
                        "Token": token.key,
                        "SessionID": session_id
                    })
                else:
                    return Response({
                        'status':400,
                        'message': 'Login Failed, check your login details and try again',
                        'error': serializer.error_messages
                    })            

    return Response({
        'status':200,
        'message': 'Welcome to login endpoint on the DHMS API',
        # 'error': serializer.error_messages
    })
    


@api_view(['GET'])
def User_Logout(request):
    # request.user.auth_token.delete()
    logout(request)
    return Response({
        "status": 200,
        "message": "Logout successfull"
    })
        # csrf_token = request.COOKIES['csrftoken']
        # userToLogout = LogoutSerializer(data = int(pk))
        # if userToLogout:
            # # SelectedUser = SignupForm.objects.get(id=pk)
            # logout(request)
            # return Response({
            #     "status": 200,
            #     "message": "Logout successfull"
            # })
        # else:
        #     return Response({
        #         "status": 400,
        #         "message": "This user not find"
        #     })

    

@swagger_auto_schema(methods=['post'], request_body=RegisterSerializer)
@api_view(['POST', 'GET'])
def Register_Org(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            companyEmail = serializer.data['email']
            companyPhone = serializer.data['phone']
            companyCity = serializer.data['city']
            password = serializer.data['password']
            retypepassword = serializer.data['repassword']
            companyName = serializer.data['companyname']
            companyUniqueID = (companyName+'-'+companyEmail).replace(" ", "")
            
            checkPhone = SignupForm.objects.filter(phone = companyPhone)
            checkEmail = SignupForm.objects.filter(email = companyEmail)
            checkEmailGen = User.objects.filter(email = companyEmail)
            checkName = SignupForm.objects.filter(companyname = companyName)
            checkNameGen = User.objects.filter(username = companyName)
            if password != retypepassword:
                return Response({
                    "status": 400,
                    "message": "Passwords do not match"
                })
                
            if checkEmail or checkEmailGen:
                return Response({
                    "status": 400,
                    "message": "Email address is in use"
                })
                
            if checkName or checkNameGen:
                return Response({
                    "status": 400,
                    "message": "Company name is in use"
                })            
            
                
            if checkPhone:
                return Response({
                    "status": 400,
                    "message": "Phone number is in use"
                })            
            
            form = SignupForm(companyname= companyName, companyUniqueID=companyUniqueID, email = companyEmail, 
            phone = companyPhone,  city =  companyCity, password = password, repassword = retypepassword)
            user = User.objects.create_user(username=companyName, email=companyEmail, password=password, first_name=companyPhone, last_name=companyUniqueID)
    
            form.save()
            user.save()
            return Response({
                "status": 200,
                "message": "Organization registration successfull.",
                "data": serializer.data
            })
        
    return Response({
        "status": 200,
        "message": "Welcome to the organization registeration page.",
    })


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def Org_Profile(request):
    if request.method == 'GET':        
        OrgProperMain = request.user.username
        if OrgProperMain:
            print(OrgProperMain)
            print(request.user)
            OrgProper = SignupForm.objects.get(companyname = OrgProperMain)
            print(OrgProper)
            if OrgProper:            
                serializer = RegisterSerializer(OrgProper, many = False)
                print(serializer)
                return Response({
                    "status": 200,
                    "message": "Organization profile details found.",
                    "data": serializer.data
                })
                
            else:
                return Response({
                    "status": 400,
                    "message": "Organization profile details not found.",
                    "error": serializer.error_messages
                })
                
            
        return Response({
            "status": 400,
            "message": "You are not logged in. Login to view your profile details",
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def View_All_Devices(request):
    if request.method == 'GET':
        AllDevices = DeviceRegisterUpload.objects.all()
        serializer = AllDevicesSerializer(AllDevices, many=True)
        return Response({
            "status":200,
            # "Count": serializer.len(),
            "message": "Device Found",
            "Data": serializer.data
        })

    return Response({
        "status":200,
        "message": "An error occured",
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def View_Org_All_Devices(request, UniqueID):
    FindOrgDevices = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = UniqueID)
    if FindOrgDevices:
        serializer = AllDevicesSerializer(FindOrgDevices, many=True)
        if serializer:
            return Response({        
                "status": 200,
                "message": "Organization's Device Found",
                "Data": serializer.data
            })
        return Response({        
            "status": 200,
            "message": "Find a specific organization's devices"
        })
    else:
        return Response({        
            "status": 400,
            "message": "Organization Not Found"
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def View_Org_Staff(request, UniqueID):
    if request.method == 'GET':
        print(UniqueID)
        FindOrgStaffMembers = StaffDataSet.objects.filter(CompanyUniqueCode = UniqueID)
        if FindOrgStaffMembers:
            serializer = StaffDataSetSerializer(FindOrgStaffMembers, many=True)
            if serializer:
                return Response({
                    "status":200,
                    "message": "Staff members found",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":400,
                    "message": "Staff members not found for this user",
                })
        
        return Response({
            "status": 400,
            "message": "An error occured. Unique ID does not exist."
        })
    
    return Response({
        "status": 200,
        "message": "Welcome back."
    })


@api_view(['GET'])
def View_All_Staff(request):
    if request.method == 'GET':
        FindOrgStaffMembers = StaffDataSet.objects.all()
        if FindOrgStaffMembers:
            serializer = StaffDataSetSerializer(FindOrgStaffMembers, many=True)
            if serializer:
                return Response({
                    "status":200,
                    "message": "Staff members found",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":400,
                    "message": "Staff members not found for this user",
                })
        
        return Response({
            "status": 400,
            "message": "An error occured."
        })
    
    # return Response({
    #     "status": 200,
    #     "message": "Welcome back."
    # })


# import requests
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# @csrf_exempt
def Register_Staff(request):
    randomNumberForStaff = random.randint(1000, 99999)
    StaffUniqueId = 'Staff-'+ request.user.username + str(randomNumberForStaff)
    if request.method == 'POST':
        print(request.user.last_name)
        if request.user.last_name:
            serializer = StaffDataSetSerializer(data = request.data, many=False)
            if serializer.is_valid():
                staff_firstname = serializer.data['staff_firstname']
                staff_lastname = serializer.data['staff_lastname']
                staff_phonenumber = serializer.data['staff_phonenumber']
                staff_email = serializer.data['staff_email']
                staff_location = serializer.data['staff_location']
                # companyUniqueID2 = serializer.data['staff_companyID']
                companyUniqueID = request.user.last_name
                staff_role = serializer.data['staff_role']
                StaffID = StaffUniqueId                

                form = StaffDataSet(CompanyUniqueCode=companyUniqueID, staff_firstname = staff_firstname, staff_lastname = staff_lastname,
                staff_phonenumber = staff_phonenumber,  staff_email =  staff_email, staff_location = staff_location, staff_role=staff_role,
                StaffID=StaffID)          
                form.save()
                return Response({
                    "status" : 200, 
                    "message" : "Staff members registered successfully",
                    "Data": serializer.data
                    })               
            
            else:
                return Response({
                    "status" : 400, 
                    "message" : "Request is invalid",
                    "error": serializer.error_messages
                    })   
            
        else:
            return Response({
                "status" : 400, 
                "message" : "The company is not regcognized"
                })                
            
    return Response({
        "status":200, 
        "message":"Welcome to the staff registeration section of this API"
        })


# TOKEN CONFIGS STARTS HERE
#this return left time
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time

# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)

# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user = token.user)
    return is_expired, token

# TOKEN CONFIGS ENDS HERE

# ORGANIZATION DHMS API ENDS HERE


# STUDENT DHMS API STARTS HERE


# StudentDHMSSignUp
@swagger_auto_schema(methods=['post'], request_body=Student_Registration_Serializer)
@api_view(['POST'])
def Student_Registration(request):    
    """
    Student registration Endpoint

    Allow students to register via the API by providing the following details:
    Username, email, name, phone number, and password
    """

    if request.method == 'POST':
        serializer = Student_Registration_Serializer(data = request.data)
        if serializer.is_valid():
            student_email = serializer.data['student_email']
            # student_username = serializer.data['student_username']
            student_name = serializer.data['student_name']
            student_school = serializer.data['student_school']
            student_password = serializer.data['student_password']
            # student_retypepassword = serializer.data['password']
            
            # checkPhone = StudentDHMSSignUp.objects.filter(student_phone = student_phone)
            checkEmail = StudentDHMSSignUp.objects.filter(student_email = student_email)
            checkEmailGen = User.objects.filter(email = student_email)
            checkName = StudentDHMSSignUp.objects.filter(student_name = student_name)
            # checkNameGen = User.objects.filter(username = student_username)
            # if student_password != student_retypepassword:
            #     return Response({
            #         "status": 400,
            #         "message": "Passwords do not match"
            #     })
                
            if checkEmail or checkEmailGen:
                return Response({
                    "status": 400,
                    "message": "Email address already exists"
                })
                
            if checkName:
                return Response({
                    "status": 400,
                    "message": "Student name already exists"
                })

            # ActivateUserBeforeRegister(student_email, code='1234')
            try:
                form = StudentDHMSSignUp( student_name=student_email, student_school=student_school, student_email = student_email, 
                student_password = student_password)

                userprofile = User.objects.create_user(username = student_email, first_name = student_name, email = student_email, 
                                last_name = student_school, password = student_password)

                form.save()
                userprofile.save()
                return Response({
                    "status": 200,
                    "message": "Student profile created successfull.",
                    "data": serializer.data
                })
            
            except:
                return Response({
                    "status": 400,
                    "message": "An error ocured, please try again"
                }) 
            
            


# STUDENT LOGIN ENDPOINT
# import requests
@swagger_auto_schema(methods=['post'], request_body=StudentLoginSerializer)
@api_view(['POST'])
def Student_Login(request):
    """
    Student Login Endpoint

    Allow students to login via the API by providing the following details:
    Email and Password
    """
     
    if request.method == 'POST':   
        serializer = StudentLoginSerializer(data = request.data)

        if serializer.is_valid():
            student_email = serializer.data['email']
            student_password = serializer.data['password']
            CheckUserAvaibility = StudentDHMSSignUp.objects.get(student_email = student_email)
            CheckUserModelAvaibility = User.objects.get(email = student_email)
            CheckUserUsername = User.objects.get(email = student_email).username

            if CheckUserAvaibility is None:
                return Response({
                    'status':400,
                    'message': 'Email and password do not match, Try again',
                    'error': serializer.error_messages
                })
            elif CheckUserModelAvaibility is None:
                return Response({
                    'status':400,
                    'message': 'User with the details you entered does not exist',
                    'error': serializer.error_messages
                })
            else:
                student_user = authenticate(request, username=CheckUserUsername, password=student_password)
                token, created = Token.objects.get_or_create(user=student_user)
                
                # Student_username = StudentDHMSSignUp.objects.get(student_email = student_email).student_username
                Student_name = StudentDHMSSignUp.objects.get(student_email = student_email).student_name
                student_school = StudentDHMSSignUp.objects.get(student_email = student_email).student_school
                
                if student_user is not None:
                    # print('login successful')
                    login(request, student_user)
                    # After successful login, retrieve the session ID
                    session_id = request.session.session_key
                    # print(session_id)
                    return Response({
                        'status':200,
                        'message': 'Student Login was Successfull',
                        "Token": token.key,
                        "SessionID": session_id,
                        "studentData": {"email": student_email, "studentName":  Student_name, "student_school": student_school},
                    })
                else:
                    return Response({
                        'status':400,
                        'message': 'Login Failed, check your login details and try again',
                        'error': serializer.error_messages
                    })            

    return Response({
        'status':200,
        'message': 'Welcome to login endpoint for student DHMS',
        # 'error': serializer.error_messages
    })
    



@swagger_auto_schema(methods=['post'], request_body=UpdatePasswordSerializer)
@api_view(['POST'])
def RequestPasswordUpdate(request):
    """
    Password update request Endpoint

    Allow users to update their password via the API by providing the follwoing information:
    Email Address
    """
    serializer = UpdatePasswordSerializer(data = request.data)
    # password_reset_form = PasswordResetForm(request.POST)
    if serializer.is_valid():
        data = serializer.data['email']
        userEmail = User.objects.get(email=data).email
        user = User.objects.get(email=data)
        print(user)
        if user:
            subject = "DHMS Password Reset Requested"
            email_template_name = "password/password_reset_email.txt"
            c = {
            "email":user,
            'domain':'itservicedeskafrica.com',
            'site_name': 'dhms@itservicedeskafrica.com',
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': default_token_generator.make_token(user),
            'protocol': 'https' if request.is_secure() else 'https',
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, 'info@itservicedeskafrica.com' , [userEmail], fail_silently=False)

                if send_mail:                        
                    return Response({
                        'status': 200,
                        'message': 'Password update email has been sent to you inbox',
                        'User': userEmail
                    })

            except:
                return Response({
                    'status': 400,
                    'message': 'Could not start process. Please try again',
                    'error': serializer.error_messages
                })
        else:
            return Response({
                'status': 400,
                'message': 'An error occured. Please try again',
                'error': serializer.error_messages
            })
        
    else:
        return Response({
            'status': 400,
            'message': 'An error occured. Please try again',
            'error': serializer.error_messages
        })











