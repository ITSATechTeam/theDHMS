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
from django.utils.crypto import get_random_string

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


# find student signup here
@swagger_auto_schema(methods=['post'], request_body=Student_Registration_Serializer)
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

                    userprofile = User.objects.create_user(username = f'{student_email} {student_name}', first_name = student_name, email = student_email, 
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
@api_view(['POST'])
def Student_Login(request):
    """
    Student Login Endpoint

    Allow students to login via the API by providing the following details:
    Email and Password
    """
     
    if request.method == 'POST':   
        serializer = StudentLoginSerializer(data = request.data)
        try:
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
                if CheckUserModelAvaibility is None:
                    return Response({
                        'status':400,
                        'message': 'User with the details you entered does not exist',
                        'error': serializer.error_messages
                    })
                else:
                    student_user = authenticate(request, username=CheckUserUsername, password=student_password)
                    print(f'{student_email} {student_password}')
                    print('student_user')
                    print('student_user')
                    print('student_user')
                    print('CheckUserModelAvaibility')
                    print(student_user)
                    token, created = Token.objects.get_or_create(user=student_user)
                    
                    # Student_username = StudentDHMSSignUp.objects.get(student_email = student_email).student_username
                    Student_name = StudentDHMSSignUp.objects.get(student_email = student_email).student_name
                    student_school = StudentDHMSSignUp.objects.get(student_email = student_email).student_school
                    student_phoneNumber = StudentDHMSSignUp.objects.get(student_email = student_email).student_phone
                    
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
                        "studentData": {"email": student_email, "Phone number": student_phoneNumber, "studentName":  Student_name, "student_school": student_school},
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
        except Exception as e:
            return Response({
                'status':400,
                'message': 'Login Failed, request was unable to process',
                "error": serializer.error_messages
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


# Technical partners serializer
@swagger_auto_schema(methods=['GET'])
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
                    # {
                    #     'Technicial_name': serializer.data.technicianName,
                    #     'Technicial_email': serializer.data.technicianEmail,
                    #     'Technicial_phone': serializer.data.technicianPhoneNumber,
                    #     'Technicial_availability': serializer.data.technicianAvailability,
                    #     'Technicial_location': serializer.data.technicianLocation,
                    #     'Technicial_ID': serializer.data.technicianUniqueID,
                    #     'Technicial_date_registered': serializer.data.created_at,
                    # }
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
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Student_Device_Registration(request):    
    """
    Student device registration Endpoint

    We allow student admins to register devices via this endpoint
    """

    if request.method == 'POST':
        try:
            serializer = StudentDeviceRegSerializer(data = request.data)
            if serializer.is_valid():
                student_admin_email = request.user.email
                student_user_email = serializer.data['student_user_email']
                student_device_name = serializer.data['device_name']
                student_device_serial_number = serializer.data['device_serial_number']
                student_device_os = serializer.data['device_os']

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
                
                checkAdminEmail = StudentDHMSSignUp.objects.filter(student_email = student_admin_email)
                checkStudentUserEmail = SubStudentRegistration.objects.filter(sub_student_email = student_user_email)
                checkAdminUserEmailGen = User.objects.filter(email = student_admin_email)
                checkDeviceSerialNumber = StudentDeviceReg.objects.filter(device_serial_number = student_device_serial_number)
                findStudentUserEmail = checkStudentUserEmail.values_list('sub_student_admin_email', flat=True)
                findStudentUserEmailMain = findStudentUserEmail[0]
                    
                if checkAdminEmail is None or checkAdminUserEmailGen is None:
                    return Response({
                        "status": 400,
                        "message": "Student Admin Email address was not found",
                        "error_message": serializer.error_messages
                    })
                
                if findStudentUserEmailMain != request.user.email:
                    return Response({
                        "status": 400,
                        "message": "The sub student is not allocated to you as the student admin, and therefore can not assign a device to the student. Kindly select a student under your allocation or register a new student",
                        "error_message": serializer.error_messages
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
                    device_os = student_device_os, student_user_email = student_user_email)
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
        except:
            return Response({
                "status": 400,
                "message": "An error ocured and device could not be registered. Kindly try again and provide all required details",
                "error": serializer.error_messages
            }) 



@swagger_auto_schema(methods=['post'], request_body=SubStudentRegistrationSerializer)
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
                sub_student_name = serializer.data['sub_student_name']
                sub_student_email = serializer.data['sub_student_email']
                checkEmailExit = SubStudentRegistration.objects.filter(sub_student_email = sub_student_email)
                checkEmailExitInUser = User.objects.filter(email = sub_student_email)
                checkEmailOfAdminStudent = StudentDHMSSignUp.objects.filter(student_email = StudentAdminEmail)
                Sub_Student_UniqueID = 'substudent' + '-' +  get_random_string(length=7)

                if(sub_student_email is None):
                    return Response({
                        "status": 400,
                        "message": "Missing student email address",
                        "error_message": serializer.error_messages
                    })
                if(sub_student_name is None):
                    return Response({
                        "status": 400,
                        "message": "Missing student name",
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
                # if(student_password is None):
                #     return Response({
                #         "status": 400,
                #         "message": "Password missing",
                #         "error_message": serializer.error_messages
                #     })

                # ActivateUserBeforeRegister(student_email, code='1234')
                try:
                    substudentformreg = SubStudentRegistration(user=request.user, sub_student_name = sub_student_name, sub_student_email=sub_student_email, 
                    sub_student_admin_email = StudentAdminEmail, sub_student_password = Sub_Student_UniqueID)

                    substudentuserprofilecreation = User.objects.create_user(username = f'{sub_student_email} {sub_student_name}', first_name = sub_student_name, email = sub_student_email, 
                                    last_name = StudentAdminEmail, password = Sub_Student_UniqueID)

                    substudentformreg.save()
                    substudentuserprofilecreation.save()
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
    # sub_student_admin_email = request.user.email
    pass





