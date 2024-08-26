import os
from venv import logger
from django.dispatch import receiver
from grpc import Status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

# from dhmsapiapp.activateuser import ActivateUserBeforeRegister
from .serializers import *
from useronboard.models import SignupForm
from userarea.models import *
from dhmsadminboard.models import *
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
from django.views.decorators.csrf import csrf_exempt


# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

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
from django.utils.crypto import get_random_string

# from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMessage



# from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer, TokenRefreshView)


# REFRESH JWT TOKEN
@swagger_auto_schema(methods=['post'], request_body=CustomTokenObtainPairSerializer)
@api_view(['POST'])
def CustomTokenObtainPair(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data)

    if serializer.is_valid():
        return Response(serializer.validated_data, status=200)
    else:
        return Response(serializer.errors, status=400)



# import requests
@csrf_exempt
@api_view(['POST', 'GET'])
def User_Login(request):
        
    try:
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
    except: Response({
            'status':500,
            'message': 'An error occured. Please try again',
            #
        })
    


@csrf_exempt
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
@csrf_exempt
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


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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


# find student signup here
@swagger_auto_schema(methods=['post'], request_body=Student_Registration_Serializer)
@csrf_exempt
@api_view(['POST'])
def Student_Registration(request):    
    """
    Student registration Endpoint

    Allow students to register via the API by providing the following details:
    email, name, phone number, and password
    """

    if request.method == 'POST':
        try:
            serializer = Student_Registration_Serializer(data = request.data)
            if serializer.is_valid():
                student_email = serializer.data['student_email']
                student_phone = serializer.data['student_phone']
                student_name = serializer.data['student_name']
                student_school = serializer.data['student_school']
                student_password = serializer.data['student_password']

                if(student_email is None):
                    return Response({
                        "status": 400,
                        "message": "Missing email address",
                        "error_message": serializer.error_messages
                    })
                if(student_phone is None):
                    return Response({
                        "status": 400,
                        "message": "Missing phone number",
                        "error_message": serializer.error_messages
                    })
                if(student_name is None):
                    return Response({
                        "status": 400,
                        "message": "No student name provided",
                        "error_message": serializer.error_messages
                    })
                if(student_school is None):
                    return Response({
                        "status": 400,
                        "message": "Kindy provide your school",
                        "error_message": serializer.error_messages
                    })
                if(student_password is None):
                    return Response({
                        "status": 400,
                        "message": "Password missing",
                        "error_message": serializer.error_messages
                    })
                
                checkEmail = StudentDHMSSignUp.objects.filter(student_email = student_email)
                checkEmailGen = User.objects.filter(email = student_email)
                checkPhone = StudentDHMSSignUp.objects.filter(student_phone = student_phone)
                    
                if checkEmail or checkEmailGen:
                    return Response({
                        "status": 400,
                        "message": "Email address already exists",
                        "error_message": serializer.error_messages
                    })
                    
                if checkPhone:
                    return Response({
                        "status": 400,
                        "message": "Student phone number already exists",
                        "error_message": serializer.error_messages
                    })

                # ActivateUserBeforeRegister(student_email, code='1234')
                try:
                    form = StudentDHMSSignUp(student_name=student_name, student_phone = student_phone, student_school=student_school, student_email = student_email, 
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
            else:
                return Response({
                    'status':400,
                    'message': 'Login Failed, check your login details and try again',
                    'error': serializer.error_messages
                })            
        except:
            return Response({
                "status": 400,
                "message": "An error ocured, kindly fill the form properly",
                "error": serializer.error_messages
            }) 


# STUDENT LOGIN ENDPOINT
# import requests
@swagger_auto_schema(methods=['post'], request_body=StudentLoginSerializer)
# @swagger_auto_schema(methods=['post'], request_body=CustomTokenObtainPairSerializer)
@csrf_exempt
@api_view(['POST'])
def Student_Login(request):
    """
    Student Login Endpoint

    Allow students to login via the API by providing the following details:
    Email and Password
    """
     
    try:
        if request.method == 'POST':   
            serializer = StudentLoginSerializer(data = request.data)
            # try:
            if serializer.is_valid():
                student_email = serializer.data['username']
                student_password = serializer.data['password']
    
                # Admin student Login setup starts here
                if StudentDHMSSignUp.objects.filter(student_email = student_email).exists():
                    CheckAdminUserAvaibility = StudentDHMSSignUp.objects.filter(student_email = student_email)
                    # All student Login setup starts here
                    CheckUserModelAvaibility = User.objects.get(email = student_email)
                    CheckUserUsername = User.objects.get(email = student_email).username
                    
                    token_serializer = CustomTokenObtainPairSerializer(data=request.data)
                    token_serializer.is_valid(raise_exception=True)
    
                    # Return the JWT token
                    # return Response(token_serializer.validated_data, status=200)
                    # return Response(token_serializer.validated_data, status=status.HTTP_200_OK)
    
    
                    if CheckAdminUserAvaibility:
                        is_Student_Admin = True
                    else:
                        is_Student_Admin = False
                        
                    if CheckAdminUserAvaibility is None:
                        return Response({
                            'status':400,
                            'message': 'Email and password do not match, Try again',
                            'error': serializer.error_messages
                        })
                    if CheckUserModelAvaibility is None:
                        return Response({
                            'status':400,
                            'message': 'User with the details you entered does not exist',
                            'error': serializer.error_messages
                        })
                    else:
                        student_user = authenticate(request, username=CheckUserUsername, password=student_password)
                        print(f'{student_email} {student_password}')
                        print('admin student access detected')
                        print(student_user)
                        # token, created = Token.objects.get_or_create(user=student_user)
                        
                        # Student_username = StudentDHMSSignUp.objects.get(student_email = student_email).student_username
                        Student_name = StudentDHMSSignUp.objects.get(student_email = student_email).student_name
                        student_school = StudentDHMSSignUp.objects.get(student_email = student_email).student_school
                        student_phoneNumber = StudentDHMSSignUp.objects.get(student_email = student_email).student_phone
                        
                    if student_user is not None:
                        # print('login successful')
                        login(request, student_user)
                        # After successful login, retrieve the session ID
                        # session_id = request.session.session_key
                        # print(session_id)
                        return Response({
                            'status':200,
                            'message': 'Student Login was Successfull',
                            "Token": token_serializer.validated_data,
                            # "SessionID": session_id,
                            "studentData": {"email": student_email, "Phone number": student_phoneNumber, "studentName":  Student_name, 
                                            "student_school": student_school, "is_student_admin": is_Student_Admin},
                        })
    
                # Sub student Login setup starts here
                elif SubStudentRegistration.objects.filter(sub_student_email_address = student_email).exists():
                    # All student Login setup starts here
                    CheckUserModelAvaibility = User.objects.get(email = student_email)
                    CheckUserUsername = User.objects.get(email = student_email).username
                    is_Student_Admin = False
                    CheckSubStudentAvaibility = SubStudentRegistration.objects.get(sub_student_email_address = student_email)
                    
                    token_serializer = CustomTokenObtainPairSerializer(data=request.data)
                    token_serializer.is_valid(raise_exception=True)
                        
                    if CheckSubStudentAvaibility is None:
                        return Response({
                            'status':400,
                            'message': 'Email and password do not match, Try again',
                            'error': serializer.error_messages
                        })
                    if CheckUserModelAvaibility is None:
                        return Response({
                            'status':400,
                            'message': 'User with the details you entered does not exist',
                            'error': serializer.error_messages
                        })
                    else:
                        student_user = authenticate(request, username=CheckUserUsername, password=student_password)
                        print(f'{student_email} {student_password}')
                        print('Sub student access detected')
                        print(student_user)
                        # token, created = Token.objects.get_or_create(user=student_user)
                        
                        # Student_username = StudentDHMSSignUp.objects.get(student_email = student_email).student_username
                        Student_name_details = SubStudentRegistration.objects.get(sub_student_email_address = student_email)
                        student_firstname = Student_name_details.sub_student_firstname
                        student_lastname = Student_name_details.sub_student_lastname
                        student_email = Student_name_details.sub_student_email_address
                        student_matric_number = Student_name_details.sub_student_matric_number
                        student_school = Student_name_details.sub_student_school_name
                        student_phoneNumber = Student_name_details.sub_student_phone_number
                        
                    if student_user is not None:
                        # print('login successful')
                        login(request, student_user)
                        # After successful login, retrieve the session ID
                        session_id = request.session.session_key
                        # print(session_id)
                        return Response({
                            'status':200,
                            'message': 'Sub Student Login was Successfull',
                            "Token": token_serializer.validated_data,
                            # "SessionID": session_id,
                            "studentData": {"email": student_email, "Phone number": student_phoneNumber, "studentFirstName":  student_firstname,"studentLastName":  student_lastname, 
                                            "student_school": student_school, "student_matric_number":student_matric_number, "is_student_admin": is_Student_Admin},
                        })
                else:
                    return Response({
                        'status':400,
                        'message': 'Login Failed, check your login details and try again',
                        'error': serializer.error_messages
                    })
    
            
            else:
                return Response({
                    'status':400,
                    'message': 'Login Failed, check your login details and try again',
                    'error': serializer.error_messages
                })  
    except: 
            return Response({
                'status':400,
                'message': 'Login Failed, check your login details and try again',
                # 'error': serializer.error_messages
            })  


@swagger_auto_schema(methods=['post'], request_body=UpdatePasswordSerializer)
@csrf_exempt
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


# Technical partners serializer
@swagger_auto_schema(methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Technical_Partners(request):
    """
    View all technical partners endpoint

    You can view all technical partners from here when you're logged in and authenticated
    """

    if request.method == 'GET':
        AllTechnicalPartners = technicianModel.objects.all()
        if AllTechnicalPartners:
            serializer = TechnicalPartnersSerializer(AllTechnicalPartners, many=True)
            if serializer:
                userData = serializer.data
                return Response({
                    "status":200,
                    "message": "Technical Partners found",
                    "data": userData
                })
            else: 
                return Response({
                    "status":400,
                    "message": "Technical Partners not found",
                })
        
        return Response({
            "status": 400,
            "message": "An error occured. No technical partner found."
        })
    
    return Response({
        "status": 200,
        "message": "Execute to view all technical partners on the DHMS."
    })


# Find a particular technical partner
@swagger_auto_schema(methods=['post'], request_body=SingleTechnicalPartnersModelSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Find_Technical_Partner(request):
    """
    View a single technical partner endpoint

    You can view or search for a single technical partners by providing their email address
    Sample Technical Partner: testpartner4@gmail.com
    """
    if request.method == 'POST':
        serializer = SingleTechnicalPartnersModelSerializer(data = request.data)
        try:
            if serializer.is_valid():
                partner_email = serializer.data['technicianEmail']

                print(partner_email)
                FindTechnicalPartner = technicianModel.objects.get(technicianEmail = partner_email)
                if FindTechnicalPartner:
                    # serializer = SingleTechnicalPartnersModelSerializer(FindTechnicalPartner, many=False)
                    if FindTechnicalPartner:
                        return Response({
                            "status":200,
                            "message": "Technical partner was found",
                            "data": {
                                'Technicial_Name' : FindTechnicalPartner.technicianName,
                                'Technicial_Email' : FindTechnicalPartner.technicianEmail,
                                'Technicial_Location' : FindTechnicalPartner.technicianLocation,
                                'Technicial_Phone' : FindTechnicalPartner.technicianPhoneNumber,
                                'Technicial_Availability' : FindTechnicalPartner.technicianAvailability,
                                'Technicial_Onboard_Date' : FindTechnicalPartner.created_at,
                            }
                        })
                    else: 
                        return Response({
                            "status":400,
                            "message": "Technical Partner not found",
                        })
                
                return Response({
                    "status": 400,
                    "message": "An error occured. Technical Partner does not exit on the DHMS"
                })
            
            return Response({
                "status": 200,
                "message": "Find Individual Technical Partners."
            })
        except:                
            return Response({
                "status": 400,
                "message": "An error occured. Technical Partner does not exit on the DHMS"
            })



@swagger_auto_schema(methods=['post'], request_body=StudentDeviceRegSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Student_Device_Registration(request):    
    """
    Student device registration Endpoint

    We allow student admins to register devices via this endpoint
    """

    if request.method == 'POST':
        # try:
        serializer = StudentDeviceRegSerializer(data = request.data)
        if serializer.is_valid():
            student_admin_email = request.user.email
            student_user_email = serializer.data['student_user_email']
            student_device_name = serializer.data['device_name']
            student_device_serial_number = serializer.data['device_serial_number']
            student_device_os = serializer.data['device_os']
            student_device_health = serializer.data['student_device_health']

            if(student_admin_email is None):
                return Response({
                    "status": 400,
                    "message": "Login as a student admin to register a device via the student DHMS",
                    "error_message": serializer.error_messages
                })
            if(student_user_email is None):
                return Response({
                    "status": 400,
                    "message": "Missing email address for student device user",
                    "error_message": serializer.error_messages
                })
            if(student_device_name is None):
                return Response({
                    "status": 400,
                    "message": "No device name was provided",
                    "error_message": serializer.error_messages
                })
            if(student_device_serial_number is None):
                return Response({
                    "status": 400,
                    "message": "No device serial number was provided",
                    "error_message": serializer.error_messages
                })
            if(student_device_os is None):
                return Response({
                    "status": 400,
                    "message": "No OS was provided",
                    "error_message": serializer.error_messages
                })
            if(student_device_health is None):
                return Response({
                    "status": 400,
                    "message": "Student device health was not provided",
                    "error_message": serializer.error_messages
                })
            
            checkAdminEmail = StudentDHMSSignUp.objects.filter(student_email = student_admin_email)
            checkAdminUserEmailGen = User.objects.filter(email = student_admin_email)
            checkDeviceSerialNumber = StudentDeviceReg.objects.filter(device_serial_number = student_device_serial_number)
            checkStudentUserEmail = SubStudentRegistration.objects.filter(sub_student_email_address = student_user_email)
            findStudentUserEmail = checkStudentUserEmail.values_list('sub_student_admin_email', flat=True)
            findStudentUserEmailMain = findStudentUserEmail.first()
                
            if checkAdminEmail is None or checkAdminUserEmailGen is None:
                return Response({
                    "status": 400,
                    "message": "Student Admin Email address was not found",
                    # "error_message": serializer.error_messages
                })
            
            if findStudentUserEmailMain != request.user.email:
                return Response({
                    "status": 400,
                    "message": "The sub student is not allocated to you as the student admin, and therefore can not assign a device to the student. Kindly select a student under your allocation or register a new student",
                    # "error_message": serializer.error_messages
                })                    
                
            if checkStudentUserEmail is None:
                return Response({
                    "status": 400,
                    "message": "Sub Student Email address was not found on the DHMS",
                    "error_message": serializer.error_messages
                })
                
            if checkDeviceSerialNumber:
                return Response({
                    "status": 400,
                    "message": "A device with the serial number already exists",
                    "error_message": serializer.error_messages
                })

            # ActivateUserBeforeRegister(student_email, code='1234')
            try:
                form = StudentDeviceReg(user=request.user, student_admin_email = student_admin_email, device_name=student_device_name, device_serial_number = student_device_serial_number, 
                device_os = student_device_os, student_user_email = student_user_email, student_device_health = student_device_health)
                form.save()
                # userprofile.save()
                return Response({
                    "status": 200,
                    "message": "Device registered successfully.",
                    "data": serializer.data
                })
            
            except:
                return Response({
                    "status": 400,
                    "message": "An error ocured, please try again"
                })            
        else:
            return Response({
                'status':400,
                'message': 'Submission error, kindly try again',
                'error': serializer.error_messages
            })            
        # except:
        #     return Response({
        #         "status": 400,
        #         "message": "An error ocured and device could not be registered. Kindly try again and provide all required details",
        #         "error": serializer.error_messages
        #     }) 



@swagger_auto_schema(methods=['post'], request_body=SubStudentRegistrationSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Sub_Student_Registration(request):   
    """
    Sub Student registration Endpoint

    Allow admin students to register sub students via the API by providing the following details:
    student email and student full name.
    """

    if request.method == 'POST':
        try:
            serializer = SubStudentRegistrationSerializer(data = request.data)
            if serializer.is_valid():
                StudentAdminEmail = request.user.email
                sub_student_firstname = serializer.data['sub_student_firstname']
                sub_student_lastname = serializer.data['sub_student_lastname']
                sub_student_email_address = serializer.data['sub_student_email_address']
                sub_student_phone_number = serializer.data['sub_student_phone_number']
                sub_student_school_name = serializer.data['sub_student_school_name']
                sub_student_matric_number = serializer.data['sub_student_matric_number']

                checkEmailExit = SubStudentRegistration.objects.filter(sub_student_email_address = sub_student_email_address)
                checkEmailExitInUser = User.objects.filter(email = sub_student_email_address)
                checkEmailOfAdminStudent = StudentDHMSSignUp.objects.filter(student_email = StudentAdminEmail)
                Sub_Student_UniqueID = 'substudent' + '-' +  get_random_string(length=7)

                if(sub_student_email_address is None):
                    return Response({
                        "status": 400,
                        "message": "Missing student email address",
                        "error_message": serializer.error_messages
                    })
                if(sub_student_phone_number is None):
                    return Response({
                        "status": 400,
                        "message": "Missing student phone number",
                        "error_message": serializer.error_messages
                    })
                if(sub_student_school_name is None):
                    return Response({
                        "status": 400,
                        "message": "Missing student school name",
                        "error_message": serializer.error_messages
                    })
                if(sub_student_matric_number is None):
                    return Response({
                        "status": 400,
                        "message": "Missing student matric number",
                        "error_message": serializer.error_messages
                    })
                if(sub_student_firstname is None):
                    return Response({
                        "status": 400,
                        "message": "Missing student firstname",
                        "error_message": serializer.error_messages
                    })
                if(sub_student_lastname is None):
                    return Response({
                        "status": 400,
                        "message": "Missing student lastname",
                        "error_message": serializer.error_messages
                    })
                if checkEmailExit or checkEmailExitInUser:
                    return Response({
                        "status": 400,
                        "message": "Email address allocated to sub student already exist on the DHMS. Kindly use a unique email address",
                        "error_message": serializer.error_messages
                    })
                if(checkEmailOfAdminStudent is None):
                    return Response({
                        "status": 400,
                        "message": "You do not have permission to register a student. Kindly register as an admin on the student DHMS to do this",
                        "error_message": serializer.error_messages
                    })
                
                # ActivateUserBeforeRegister(student_email, code='1234')

                try:
                    substudentformreg = SubStudentRegistration(user=request.user, sub_student_firstname = sub_student_firstname, sub_student_lastname = sub_student_lastname, sub_student_email_address=sub_student_email_address, 
                    sub_student_admin_email = StudentAdminEmail, sub_student_password = Sub_Student_UniqueID, sub_student_phone_number = sub_student_phone_number, sub_student_school_name = sub_student_school_name,
                    sub_student_matric_number = sub_student_matric_number)

                    substudentuserprofilecreation = User.objects.create_user(username = sub_student_email_address, first_name = sub_student_firstname, email = sub_student_email_address, 
                                    last_name = sub_student_lastname, password = Sub_Student_UniqueID)

                    substudentformreg.save()
                    substudentuserprofilecreation.save()
                    return Response({
                        "status": 200,
                        "message": "Sub Student profile created successfull.",
                        "data": serializer.data
                    })
                
                except:
                    return Response({
                        "status": 400,
                        "message": "An error ocured, please try again"
                    })            
            else:
                return Response({
                    'status':400,
                    'message': 'Login Failed, check your login details and try again',
                    'error': serializer.error_messages
                })            
        except:
            return Response({
                "status": 400,
                "message": "An error ocured, kindly fill the form properly",
                "error": serializer.error_messages
            }) 
    # sub_student_admin_email = request.user.email



# GET ALL STUDENT ADMIN REGISTERED DEVICES ENDPOINT
@swagger_auto_schema(methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllStudentDevices(request):
    try:
        currentUserDevices = StudentDeviceReg.objects.filter(student_admin_email = request.user.email)
        if currentUserDevices:
            serializer = AllStudentDevicesSerializer(currentUserDevices, many=True)
            if serializer:
                return Response({
                    "status":200,
                    "message": "Student Devices found",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":400,
                    "message": "No device found",
                })
        
        else:
            return Response({
            "status": 400,
            "message": "No device is assigned to you."
            })

    except:
        return Response({
            "status": 400,
            "message": "You're probably not authenticated. Kindly try again"
        })



# GET SPECIFIC STUDENT ADMIN REGISTERED DEVICES ENDPOINT
@swagger_auto_schema(methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetSingleStudentDevices(request, id):
    try:
        if id:
            specificDevice = StudentDeviceReg.objects.get(Q(id = id) & Q(student_admin_email = request.user.email))
            serializer = AllStudentDevicesSerializer(specificDevice, many=False)
            if serializer:
                return Response({
                    "status":200,
                    "message": "Student Device found",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":400,
                    "message": "No device with specified ID",
                })
        else:
            Response({
            "status": 400,
            "message": "Device with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": 400,
            "message": "You're probably not authenticated. Kindly try again"
        })



# SUPER ADMIN FUNCTIONS STARTS HERE
@swagger_auto_schema(methods=['post'], request_body=ItsaSuperAdminLoginSerializer)
@csrf_exempt
@api_view(['POST'])
def ItsaSuperAdminLoginFxn(request):
    try:
        if request.method == 'POST':   
            serializer = ItsaSuperAdminLoginSerializer(data = request.data)
            # try:
            if serializer.is_valid():
                admin_email = serializer.data['email']
                admin_password = serializer.data['password']

                # Admin student Login setup starts here
                if SuperAdminsModel.objects.filter(email = admin_email).exists():
                    CheckAdminUserAvaibility = SuperAdminsModel.objects.filter(email = admin_email)              


                    # All student Login setup starts here
                    CheckUserModelAvaibility = User.objects.get(email = admin_email)
                    CheckUserUsername = User.objects.get(email = admin_email).username
                        
                    if CheckAdminUserAvaibility is None:
                        return Response({
                            'status':400,
                            'message': 'Email and password do not match, Try again',
                            'error': serializer.error_messages
                        })
                    if CheckUserModelAvaibility is None:
                        return Response({
                            'status':400,
                            'message': 'User with the details you entered does not exist',
                            'error': serializer.error_messages
                        })
                    else:
                        admin_user = authenticate(request, username=CheckUserUsername, password=admin_password)
                        token, created = Token.objects.get_or_create(user=admin_user)
                        
                        Admin_name = SuperAdminsModel.objects.get(email = admin_email).firstname
                        Admin_email = SuperAdminsModel.objects.get(email = admin_email).email
                        
                        # Get organization and device data for admin dashboard
                        AllCompany = SignupForm.objects.all()
                        AllCompanyCount = AllCompany.count()
                        AllDevices = DeviceRegisterUpload.objects.all()
                        AllDevicesCount = AllDevices.count()
                        AllFaultyDevices = DeviceRegisterUpload.objects.filter(devicestatus = 'Faulty')
                        AllFaultyDevicesCount = AllFaultyDevices.count()
                        AllHealthyDevices = DeviceRegisterUpload.objects.filter(devicestatus = 'Working')
                        AllHealthyDevicesCount = AllHealthyDevices.count()

                        # Latest registered company req. info
                        LatestRegisteredCompanyID = SignupForm.objects.all()[1:2].values_list('companyUniqueID', flat=True)[0]
                        print(LatestRegisteredCompanyID)
                        LatestRegisteredCompanyName = SignupForm.objects.all()[1:2].values_list('companyname', flat=True)[0]
                        AllLatestRegisteredCompanyDevices = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = LatestRegisteredCompanyID)
                        LatestRegCompDevices = AllLatestRegisteredCompanyDevices.count()
                        LatestRegCompFaultyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Faulty') & Q(CompanyUniqueCode = LatestRegisteredCompanyID))
                        LatestRegCompFaultyDevicesCount = LatestRegCompFaultyDevices.count()
                        LatestRegCompWorkingDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(CompanyUniqueCode = LatestRegisteredCompanyID))
                        LatestRegCompWorkingDevicesCount = LatestRegCompWorkingDevices.count()
                        LatestRegCompStaff = StaffDataSet.objects.filter(CompanyUniqueCode = LatestRegisteredCompanyID)
                        LatestRegCompStaffCount = LatestRegCompStaff.count()
                        
                    if admin_user is not None:
                        login(request, admin_user)
                        session_id = request.session.session_key
                        return Response({
                            'status':200,
                            'message': 'Admin Login was Successfull',
                            "Token": token.key,
                            "SessionID": session_id,
                            "studentData": {"email": Admin_email, "adminName":  Admin_name, 'NumberofOrg': AllCompanyCount, 'NumberofDevices': AllDevicesCount,
                                            'NumberofFaultyDevices':AllFaultyDevicesCount, 'NumberofHealthyDevices':AllHealthyDevicesCount, 'LatestRegCompDevices':LatestRegCompDevices,
                                            'LatestRegCompName':LatestRegisteredCompanyName, 'LatestRegCompFaultyDevicesCount':LatestRegCompFaultyDevicesCount, 'LatestRegCompWorkingDevicesCount':LatestRegCompWorkingDevicesCount,
                                            'LatestRegCompStaffCount':LatestRegCompStaffCount},
                        })
    except:
        return Response({
            "status": 400,
            "message": "An error occured",
            "error_message": serializer.error_messages
        })



@swagger_auto_schema(methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllRegStudents(request):
    try:
        currentUserStudents = SubStudentRegistration.objects.filter(sub_student_admin_email = request.user.email)
        if currentUserStudents:
            serializer = FetchStudentSerializer(currentUserStudents, many=True)
            if serializer:
                return Response({
                    "status":200,
                    "message": "Students found",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":400,
                    "message": "No student found",
                })
        
        else:
            Response({
            "status": 400,
            "message": "You have not registered any students yet."
            })

    except:
        return Response({
            "status": 400,
            "message": "You're probably not authenticated. Kindly try again"
        })


# GET SPECIFIC STUDENT ADMIN REGISTERED DEVICES ENDPOINT
@swagger_auto_schema(methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetSingleStudents(request, id):
    try:
        if id:
            specificStudent = SubStudentRegistration.objects.get(Q(id = id) & Q(sub_student_admin_email = request.user.email))
            serializer = FetchStudentSerializer(specificStudent, many=False)
            if serializer:
                return Response({
                    "status":200,
                    "message": "Student found",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":400,
                    "message": "No student with specified ID",
                })
        else:
            Response({
            "status": 400,
            "message": "Student with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": 400,
            "message": "Student could not be found. Kindly try again"
        })



@swagger_auto_schema(methods=['PUT'], request_body=FetchStudentSerializerForEdit)
@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['PUT'])
def EditStudentData(request, id):
    try:
        if id:
            specificStudent = SubStudentRegistration.objects.get(Q(id = id) & Q(sub_student_admin_email = request.user.email))
            serializer = FetchStudentSerializerForEdit(specificStudent, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status":200,
                    "message": "Student info updated",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":400,
                    "message": "An error occured while trying to save updates, kindly try again",
                })
        else:
            Response({
            "status": 400,
            "message": "Student with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": 400,
            "message": "An error occured. If you want, you can try again"
        })



@swagger_auto_schema(methods=['DELETE'])
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteStudentData(request, id):
    try:
        if id:
            DeviceStudent = SubStudentRegistration.objects.get(Q(id = id) & Q(sub_student_admin_email = request.user.email))
            if DeviceStudent:
                DeviceStudent.delete()
                Response({
                "status": 200,
                "message": "Student was deleted successfully."
                })
            else:
                Response({
                "status": 400,
                "message": "Student with specified ID was not found under your directory."
                })
        else:
            Response({
            "status": 400,
            "message": "Student with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": 400,
            "message": "An error occured. If you want, you can try again"
        })
    


@swagger_auto_schema(methods=['PUT'], request_body=DeviceSerializerForEdit)
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def EditDeviceData(request, id):
    try:
        if id:
            DeviceStudent = StudentDeviceReg.objects.get(Q(id = id) & Q(student_admin_email = request.user.email))
            serializer = DeviceSerializerForEdit(DeviceStudent, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status":200,
                    "message": "Device info updated",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":400,
                    "message": "An error occured while trying to save updates, kindly try again",
                })
        else:
            Response({
            "status": 400,
            "message": "Device with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": 400,
            "message": "An error occured. If you want, you can try again"
        })


@swagger_auto_schema(methods=['DELETE'])
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteDeviceData(request, id):
    try:
        if id:
            DeviceStudent = StudentDeviceReg.objects.get(Q(id = id) & Q(student_admin_email = request.user.email))
            DeviceStudent.delete()
            return Response({
            "status": 200,
            "message": "Device was deleted successfully."
            })
        else:
            return Response({
            "status": 400,
            "message": "Device with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": 400,
            "message": "An error occured. If you want, you can try again"
        })
    


@swagger_auto_schema(methods=['PUT'])
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def EditDeviceData(request, id):
    try:
        if id:
            DeviceStudent = StudentDeviceReg.objects.get(Q(id = id) & Q(student_admin_email = request.user.email))
            DeviceStudent.delete()
            return Response({
            "status": 200,
            "message": "Device was deleted successfully."
            })
        else:
            return Response({
            "status": 400,
            "message": "Device with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": 400,
            "message": "An error occured. If you want, you can try again"
        })



@swagger_auto_schema(methods=['get'])
@csrf_exempt
@api_view(['GET'])
def MaintenanceReqPerMonth(request):    
    try:
        JanMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'Jan').count()
        FebMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'Feb').count()
        MarMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'Mar').count()
        AprMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'Apr').count()
        MayMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'May').count()
        JunMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'Jun').count()
        JulMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'Jul').count()
        AugMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'Aug').count()
        SeptMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'Sep').count()
        OctMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'Oct').count()
        NovMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'Nov').count()
        DecMaintenanceCount = MaintenanceRequest.objects.filter(currentMonth = 'Dec').count()
    
        return Response({
            "status":200,
            "message": "All maintenance requests were found",
            "data": {
                'JanMaintenanceRequests' : JanMaintenanceCount,
                'FebMaintenanceRequests' : FebMaintenanceCount,
                'MarMaintenanceRequests' : MarMaintenanceCount,
                'AprMaintenanceRequests' : AprMaintenanceCount,
                'MayMaintenanceRequests' : MayMaintenanceCount,
                'JunMaintenanceRequests' : JunMaintenanceCount,
                'JulMaintenanceRequests' : JulMaintenanceCount,
                'AugMaintenanceRequests' : AugMaintenanceCount,
                'SepMaintenanceRequests' : SeptMaintenanceCount,
                'OctMaintenanceRequests' : OctMaintenanceCount,
                'NovMaintenanceRequests' : NovMaintenanceCount,
                'DevMaintenanceRequests' : DecMaintenanceCount,
            }
        })
    except:
        return Response({
            "status": 400,
            "message": "An error occured trying to find maintenance requests records"
        })



