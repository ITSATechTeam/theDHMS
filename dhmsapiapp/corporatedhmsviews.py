import json
import os
from rest_framework import status
from django.conf import settings
import hmac
import hashlib
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, schema
from dhmsapiapp.generate_code import Verify_otp, generate_validation_code
from dhmsapiapp.sendphonecode import SendPhoneVerificationCode
from dhmsapiapp.sendtransactionmails import TransferEmailNotification
from .utils import save_new_transactions
from .serializers import *
from userarea.models import *
from dhmsadminboard.models import *
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
import random
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from datetime import date, timedelta
from django.utils import timezone
from django.conf import settings
from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema
# from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMessage
paystackSecretKey = str(os.getenv('paystack_secret_key'))


# REFRESH JWT TOKEN
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['post'], request_body=CustomTokenObtainPairSerializer)
@api_view(['POST'])
def CustomTokenObtainPair(request):
    serializer = CustomTokenObtainPairSerializer(data=request.data)

    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# import requests
@csrf_exempt
@api_view(['POST', 'GET'])
def User_Login(request):
    try:
        # RegisterSerializer
        if request.method == 'POST':   
            serializer = OrgLoginSerializer(data = request.data)            
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']
                CheckUserAvaibility = SignupForm.objects.get(email = email)
                CheckUserModelAvaibility = User.objects.get(email = email)
                CheckUserUsername = User.objects.get(email = email).username
                if CheckUserAvaibility is None:
                    return Response({
                        'status':status.HTTP_400_BAD_REQUEST,
                        'message': 'Email and password do not match, Try again',
                        # 'error': serializer.error_messages
                    })
                elif CheckUserModelAvaibility is None:
                    return Response({
                        'status':status.HTTP_400_BAD_REQUEST,
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
                            'status':status.HTTP_200_OK,
                            'message': 'Login Successfull',
                            "Token": token.key,
                            "SessionID": session_id
                        })
                    else:
                        return Response({
                            'status':status.HTTP_400_BAD_REQUEST,
                            'message': 'Login Failed, check your login details and try again',
                            'error': serializer.error_messages
                        })            

        return Response({
            'status':status.HTTP_200_OK,
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
@schema(None)  
def User_Logout(request):
    # request.user.auth_token.delete()
    logout(request)
    return Response({
        "status": status.HTTP_200_OK,
        "message": "Logout successfull"
    })
        # csrf_token = request.COOKIES['csrftoken']
        # userToLogout = LogoutSerializer(data = int(pk))
        # if userToLogout:
            # # SelectedUser = SignupForm.objects.get(id=pk)
            # logout(request)
            # return Response({
            #     "status": status.HTTP_200_OK,
            #     "message": "Logout successfull"
            # })
        # else:
        #     return Response({
        #         "status": status.HTTP_400_BAD_REQUEST,
        #         "message": "This user not find"
        #     })

    

@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['post'], request_body=RegisterSerializer)
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
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Passwords do not match"
                })
                
            if checkEmail or checkEmailGen:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Email address is in use"
                })
                
            if checkName or checkNameGen:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Company name is in use"
                })            
            
                
            if checkPhone:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Phone number is in use"
                })            
            
            form = SignupForm(companyname= companyName, companyUniqueID=companyUniqueID, email = companyEmail, 
            phone = companyPhone,  city =  companyCity, password = password, repassword = retypepassword)
            user = User.objects.create_user(username=companyName, email=companyEmail, password=password, first_name=companyPhone, last_name=companyUniqueID)
    
            form.save()
            user.save()
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Organization registration successfull.",
                "data": serializer.data
            })
        
    return Response({
        "status": status.HTTP_200_OK,
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
                    "status": status.HTTP_200_OK,
                    "message": "Organization profile details found.",
                    "data": serializer.data
                })
                
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Organization profile details not found.",
                    "error": serializer.error_messages
                })
                
            
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
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
            "status":status.HTTP_200_OK,
            # "Count": serializer.len(),
            "message": "Device Found",
            "Data": serializer.data
        })

    return Response({
        "status":status.HTTP_200_OK,
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
                "status": status.HTTP_200_OK,
                "message": "Organization's Device Found",
                "Data": serializer.data
            })
        return Response({        
            "status": status.HTTP_200_OK,
            "message": "Find a specific organization's devices"
        })
    else:
        return Response({        
            "status": status.HTTP_400_BAD_REQUEST,
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
                    "status":status.HTTP_200_OK,
                    "message": "Staff members found",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "Staff members not found for this user",
                })
        
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Unique ID does not exist."
        })
    
    return Response({
        "status": status.HTTP_200_OK,
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
                    "status":status.HTTP_200_OK,
                    "message": "Staff members found",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "Staff members not found for this user",
                })
        
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured."
        })
    
    # return Response({
    #     "status": status.HTTP_200_OK,
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
                    "status" : status.HTTP_200_OK, 
                    "message" : "Staff members registered successfully",
                    "Data": serializer.data
                    })               
            
            else:
                return Response({
                    "status" : status.HTTP_400_BAD_REQUEST, 
                    "message" : "Request is invalid",
                    "error": serializer.error_messages
                    })   
            
        else:
            return Response({
                "status" : status.HTTP_400_BAD_REQUEST, 
                "message" : "The company is not regcognized"
                })                
            
    return Response({
        "status":status.HTTP_200_OK, 
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

