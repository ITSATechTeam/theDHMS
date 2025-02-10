import json
import os
from rest_framework import status
from django.conf import settings
import hmac
import hashlib
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, schema
from dhmsapiapp.findpartners import FindTechniciansInLocation
from dhmsapiapp.generate_code import Verify_otp, generate_validation_code
from dhmsapiapp.getlocation import get_address_from_coordinates, get_location_from_lat_long, get_location_from_lat_long_opencage
from dhmsapiapp.sendmails import SendSubStudentEmailNotification
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
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['post'], request_body=Student_Registration_Serializer)
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
                student_firstname = serializer.data['student_firstname']
                student_lastname = serializer.data['student_lastname']
                student_school = serializer.data['student_school']
                student_password = serializer.data['student_password']

                if(student_email is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing email address",
                        "error_message": serializer.error_messages
                    })
                if(student_phone is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing phone number",
                        "error_message": serializer.error_messages
                    })
                if(student_firstname is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "No student first name provided",
                        "error_message": serializer.error_messages
                    })
                    
                if(student_lastname is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "No student last name provided",
                        "error_message": serializer.error_messages
                    })
                if(student_school is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Kindy provide your school",
                        "error_message": serializer.error_messages
                    })
                if(student_password is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Password missing",
                        "error_message": serializer.error_messages
                    })
                
                checkEmail = StudentDHMSSignUp.objects.filter(student_email = student_email)
                checkEmailGen = User.objects.filter(email = student_email)
                checkPhone = StudentDHMSSignUp.objects.filter(student_phone = student_phone)
                    
                if checkEmail or checkEmailGen:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Email address already exists",
                        "error_message": serializer.error_messages
                    })
                    
                if checkPhone:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Student phone number already exists",
                        "error_message": serializer.error_messages
                    })

                # ActivateUserBeforeRegister(student_email, code='1234')
                try:
                    form = StudentDHMSSignUp(student_firstname=student_firstname, student_lastname=student_lastname, student_phone = student_phone, student_school=student_school, student_email = student_email, 
                    student_password = student_password)

                    userprofile = User.objects.create_user(username = student_email, first_name = student_firstname, email = student_email, 
                                    last_name = student_lastname, password = student_password)  
                    
                    # save user info in DB
                    form.save()
                    userprofile.save()                    
                    # Fetch data for creating tokens
                    getUserusername = student_email
                    getUserPassword = student_password

                    tokenCreationDate = {
                        'username': getUserusername,
                        'password': getUserPassword
                    }
                    token_serializer = CustomTokenObtainPairSerializer(data=tokenCreationDate)
                    token_serializer.is_valid(raise_exception=True)
                    
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Student profile created successfull.",
                        "Token": token_serializer.validated_data,
                        "data": serializer.data
                    })
                
                except:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "An error ocured, please try again"
                    })            
            else:
                return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message': 'Login Failed, check your login details and try again',
                    'error': serializer.error_messages
                })            
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "An error ocured, kindly fill the form properly",
                "error": serializer.error_messages
            }) 


# update student data here
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['PUT'], request_body=Update_Student_Registration_Serializer)
@csrf_exempt
@api_view(['PUT'])
def EditAdminStudentData(request):
    try:
        serializer = Update_Student_Registration_Serializer(data = request.data)
        currentUser = StudentDHMSSignUp.objects.get(student_email = request.user.email)
        if serializer.is_valid():
            studentFirstname = serializer.data['student_firstname']
            studentLastname = serializer.data['student_lastname']
            # studentEmail = serializer.data['student_email']
            studentSchool = serializer.data['student_school']
            studentPhone = serializer.data['student_phone']
            
            userDataToSave = {
                'student_firstname': studentFirstname, 'student_lastname':studentLastname,
                'student_school': studentSchool, 'student_phone': studentPhone
            }
            
            # CHECK IF STUDENT EXIST
            # if(StudentDHMSSignUp.objects.get(student_email = studentEmail)):
            #     return Response({
            #         "status":status.HTTP_400_BAD_REQUEST, 
            #         "message":"Email address already exist",
            #         'error':serializer.error_messages
            #     })        
            if(StudentDHMSSignUp.objects.get(student_email = request.user.email)):
                findStudentUser = User.objects.get(email = request.user.email)
                serializer = Update_Student_Registration_Serializer(currentUser, data = userDataToSave)
                if serializer.is_valid():
                    serializer.save()
                    findStudentUser.first_name = studentFirstname
                    findStudentUser.last_name = studentLastname
                    # findStudentUser.email = studentEmail
                    # findStudentUser.username = studentEmail
                    findStudentUser.save()
                    return Response({
                        "status":status.HTTP_200_OK, 
                        "message":"Your information has been updated successfully"
                        })
                else:
                    return Response({
                        "status":status.HTTP_400_BAD_REQUEST, 
                        "message":"An error occured while trying to update data",
                        'error':serializer.error_messages
                        })
            else:      
                return Response({
                    "status":status.HTTP_400_BAD_REQUEST, 
                    "message":"This user does not exit"
                    })        
        else:                    
            return Response({
                "status":status.HTTP_400_BAD_REQUEST, 
                "message":"An error occured while trying to update data",
                'error':serializer.error_messages
            })        
    except:                
        return Response({
            "status":status.HTTP_400_BAD_REQUEST, 
            "message":"An error occured while trying to update data",
        })


# STUDENT LOGIN ENDPOINT
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['POST'], request_body=StudentLoginSerializer)
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
                    print(request.data)
                    token_serializer.is_valid(raise_exception=True)
                    
                    # Check if user email is verified
                    student_admin_id = StudentDHMSSignUp.objects.get(student_email = student_email).id
                    if VerifyEmailAddress.objects.filter(studentID = student_admin_id):
                        student_email_verification_status = True
                    else:
                        student_email_verification_status = False
                    # Check if user pin is set
                    StudentID = StudentDHMSSignUp.objects.get(student_email = student_email).id
                    if StudentTransactionPIN.objects.filter(student_id = StudentID):
                        student_pin_set = True
                    else:
                        student_pin_set = False

                    if CheckAdminUserAvaibility:
                        is_Student_Admin = True
                    else:
                        is_Student_Admin = False
                        
                    if CheckAdminUserAvaibility is None:
                        return Response({
                            'status':status.HTTP_400_BAD_REQUEST,
                            'message': 'Email and password do not match, Try again',
                            'error': serializer.error_messages
                        })
                    if CheckUserModelAvaibility is None:
                        return Response({
                            'status':status.HTTP_400_BAD_REQUEST,
                            'message': 'User with the details you entered does not exist',
                            'error': serializer.error_messages
                        })
                    else:
                        student_user = authenticate(request, username=CheckUserUsername, password=student_password)
                        print('admin student access detected')
                        # token, created = Token.objects.get_or_create(user=student_user)
                        
                        # Student_username = StudentDHMSSignUp.objects.get(student_email = student_email).student_username
                        Student_firstname = StudentDHMSSignUp.objects.get(student_email = student_email).student_firstname
                        Student_lastname = StudentDHMSSignUp.objects.get(student_email = student_email).student_lastname
                        student_school = StudentDHMSSignUp.objects.get(student_email = student_email).student_school
                        student_phoneNumber = StudentDHMSSignUp.objects.get(student_email = student_email).student_phone
                        
                    if student_user is not None:
                        login(request, student_user)
                        return Response({
                            'status':status.HTTP_200_OK,
                            'message': 'Student Login was Successfull',
                            "Token": token_serializer.validated_data,
                            # "SessionID": session_id,
                            "studentData": {"email": student_email, "phone_number": student_phoneNumber, "student_firstName":  Student_firstname, 
                                            "student_lastname": Student_lastname, "student_school": student_school, 'student_email_verification_status': student_email_verification_status, 
                                            "student_pin_set":student_pin_set, "is_student_admin": is_Student_Admin},
                            })

                # Sub student Login setup starts here
                elif SubStudentRegistration.objects.filter(sub_student_email_address = student_email).exists():
                    print('sub student login triggered')
                    # All student Login setup starts here
                    CheckUserModelAvaibility = User.objects.get(email = student_email)
                    CheckUserUsername = User.objects.get(email = student_email).username
                    is_Student_Admin = False
                    CheckSubStudentAvaibility = SubStudentRegistration.objects.get(sub_student_email_address = student_email)
                    
                    token_serializer = CustomTokenObtainPairSerializer(data=request.data)
                    token_serializer.is_valid(raise_exception=True)
                        
                    if CheckSubStudentAvaibility is None:
                        return Response({
                            'status':status.HTTP_400_BAD_REQUEST,
                            'message': 'Email and password do not match, Try again',
                            'error': serializer.error_messages
                        })
                    if CheckUserModelAvaibility is None:
                        return Response({
                            'status':status.HTTP_400_BAD_REQUEST,
                            'message': 'User with the details you entered does not exist',
                            'error': serializer.error_messages
                        })
                    else:
                        student_user = authenticate(request, username=CheckUserUsername, password=student_password)                        
                        Student_name_details = SubStudentRegistration.objects.get(sub_student_email_address = student_email)
                        student_firstname = Student_name_details.sub_student_firstname
                        student_lastname = Student_name_details.sub_student_lastname
                        student_email = Student_name_details.sub_student_email_address
                        student_matric_number = Student_name_details.sub_student_matric_number
                        student_school = Student_name_details.sub_student_school_name
                        student_phoneNumber = Student_name_details.sub_student_phone_number
                        
                        
                    sub_student_id = SubStudentRegistration.objects.get(sub_student_email_address = student_email).id
                    if VerifyEmailAddress.objects.filter(studentID = sub_student_id):
                        student_email_verification_status = True
                    else:
                        student_email_verification_status = False
                        # check if PIN is created
                    if StudentTransactionPIN.objects.filter(student_id = sub_student_id):
                        student_pin_set = True
                    else:
                        student_pin_set = False

                        
                    if student_user is not None:
                        login(request, student_user)
                        return Response({
                            'status':status.HTTP_200_OK,
                            'message': 'Sub Student Login was Successfull',
                            "Token": token_serializer.validated_data,
                            "studentData": {"email": student_email, "Phone_number": student_phoneNumber, "student_firstName":  student_firstname, "student_lastname":  student_lastname, 
                                            "student_school": student_school, "student_matric_number":student_matric_number, "is_student_admin": is_Student_Admin,
                                            'student_email_verification_status': student_email_verification_status, "student_pin_set":student_pin_set,
                                            },
                        })
                else:
                    return Response({
                        'status':status.HTTP_400_BAD_REQUEST,
                        'message': 'Login Failed, check your login details and try again',
                        'error': serializer.error_messages
                    })

            
            else:
                return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message': 'Login Failed, check your login details and try again',
                }) 
        else:
                return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message': 'Login Failed, check your login details and try again',
                }) 
    except: 
        return Response({
            'status':status.HTTP_400_BAD_REQUEST,
            'message': 'Login Failed, kindly check your login details and try again',
            # 'error': serializer.error_messages
        })  


@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['post'], request_body=UpdatePasswordSerializer)
@csrf_exempt
@permission_classes([])
@api_view(['POST'])
def RequestPasswordUpdate(request):
    """
    Password update request Endpoint

    Allow users to update their password via the API by providing the follwoing information:
    Email Address
    """
    try:
        serializer = UpdatePasswordSerializer(data = request.data)
        # password_reset_form = PasswordResetForm(request.POST)
        if serializer.is_valid():
            data = serializer.data['email']
            if User.objects.get(email=data):
                userEmail = User.objects.get(email=data).email
                print('userEmail')
                print(userEmail)
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
                                'status': status.HTTP_200_OK,
                                'message': 'Password update email has been sent to your inbox',
                                'User': userEmail
                            })
                    except(KeyError):
                        return Response({
                            'status': status.HTTP_400_BAD_REQUEST,
                            'message': 'Reset password email not sent',
                            'error': KeyError
                        })
                else:
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'An error occured. Please try again',
                        'error': serializer.error_messages
                    })
            else:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Email not found',
                })        
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'An error occured. Please try again',
                'error': serializer.error_messages
            })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured. Kindly confirm email address and be sure you network is up',
        })



@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['PUT'], request_body=UpdatePasswordSerializerWithPasswordField)
@csrf_exempt
@api_view(['PUT'])
def AddNewPassword(request):
    # try:
        fetchStudentModelUser = StudentDHMSSignUp.objects.get(student_email = request.user.email)
        fetchUser = User.objects.get(email = request.user.email)
        fetchCurrentPassword = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_password
        print(fetchCurrentPassword)
        # 
        new_password = request.data['newPassword']
        old_password = request.data['oldPassword']
        
        if fetchCurrentPassword != old_password:
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "An error occured. The old password you entered is incorrect.",
                })
        elif fetchCurrentPassword == new_password:
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "An error occured. The new password you entered is same as the old password.",
                })
        
        update_password = {"student_password": request.data['newPassword']}
        serializerStudentModel = UpdatePasswordSerializerWithPasswordFieldStudentModel(fetchStudentModelUser, data = update_password)
            
        if serializerStudentModel.is_valid():
            serializerStudentModel.save()
            fetchUser.set_password(new_password)
            fetchStudentModelUser.save()
            fetchUser.save()
        else: 
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "An error with student model update. Kindly try again",
                'error': serializerStudentModel.error_messages
                    })
            
        return Response({
            "status":status.HTTP_200_OK,
            "message": "Password updated successfully",
            "data": serializerStudentModel.data
        })
    # except:                
    #     return Response({
    #         "status": status.HTTP_400_BAD_REQUEST,
    #         "message": "An error occured while trying to update password. Please try again"
    #     })
                




# Technical partners serializer
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
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
                    "status":status.HTTP_200_OK,
                    "message": "Technical Partners found",
                    "data": userData
                })
            else: 
                return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "Technical Partners not found",
                })
        
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. No technical partner found."
        })
    
    return Response({
        "status": status.HTTP_200_OK,
        "message": "Execute to view all technical partners on the DHMS."
    })


# Find a particular technical partner
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['post'], request_body=SingleTechnicalPartnersModelSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def GetTechnicalPartnerProfile(request):
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
                FindTechnicalPartner = technicianModel.objects.get(technicianEmail = partner_email)
                if FindTechnicalPartner:
                    # serializer = SingleTechnicalPartnersModelSerializer(FindTechnicalPartner, many=False)
                    if FindTechnicalPartner:
                        return Response({
                            "status":status.HTTP_200_OK,
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
                            "status":status.HTTP_400_BAD_REQUEST,
                            "message": "Technical Partner not found",
                        })
                
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "An error occured. Technical Partner does not exit on the DHMS"
                })
            
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Find Individual Technical Partners."
            })
        except:                
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "An error occured. Technical Partner does not exit on the DHMS"
            })
            

@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['post'], request_body=StudentDeviceRegSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Student_Device_Registration(request):    
    """
    Student device registration Endpoint

    We allow student admins to register devices via this endpoint
    """

    try:
        if request.method == 'POST':
            serializer = StudentDeviceRegSerializer(data = request.data)
            if serializer.is_valid():
                student_admin_id = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
                student_admin_email = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_email
                
                student_user_email = serializer.data['student_user_email']
                student_device_name = serializer.data['device_name']
                student_device_serial_number = serializer.data['device_serial_number']
                student_device_os = serializer.data['device_os']
                student_device_health = serializer.data['student_device_health']
                
                if(student_admin_email is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Login as a student admin to register a device via the student DHMS",
                        "error_message": serializer.error_messages
                    })
                if(student_user_email is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing email address for student device user",
                        "error_message": serializer.error_messages
                    })
                if(student_device_name is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "No device name was provided",
                        "error_message": serializer.error_messages
                    })
                if(student_device_serial_number is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "No device serial number was provided",
                        "error_message": serializer.error_messages
                    })
                if(student_device_os is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "No OS was provided",
                        "error_message": serializer.error_messages
                    })
                if(student_device_health is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Student device health was not provided",
                        "error_message": serializer.error_messages
                    })
                    
                # checkAdminEmail = StudentDHMSSignUp.objects.filter(student_email = student_admin_email)
                checkAdminEmail = StudentDHMSSignUp.objects.filter(student_email = student_admin_email)
                checkAdminUserEmailGen = User.objects.filter(email = student_admin_email)
                checkDeviceSerialNumber = StudentDeviceReg.objects.filter(device_serial_number = student_device_serial_number)
                checkStudentUserEmail = SubStudentRegistration.objects.filter(sub_student_email_address = student_user_email)
                findAdminUserEmail = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_email
                # findStudentUserEmailMain = findStudentUserAdminID.first()
                    
                if checkAdminEmail is None or checkAdminUserEmailGen is None:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Student Admin Email address was not found",
                        # "error_message": serializer.error_messages
                    })
                
                if findAdminUserEmail != request.user.email:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "The sub student is not allocated to you as the student admin, and therefore can not assign a device to the student. Kindly select a student under your allocation or register a new student",
                        # "error_message": serializer.error_messages
                    })
                    
                if checkStudentUserEmail is None:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Sub Student Email address is invalid",
                        "error_message": serializer.error_messages
                    })
                    
                if checkDeviceSerialNumber:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "A device with the serial number already exists",
                        "error_message": serializer.error_messages
                    })
                # check if student is assigned to the admin
                
                if int(SubStudentRegistration.objects.get(sub_student_email_address = serializer.data['student_user_email']).sub_student_admin_id) == int(student_admin_id):
                    # Find the device user ID
                    SubStudentID = SubStudentRegistration.objects.get(sub_student_email_address = serializer.data['student_user_email']).id
                    print(SubStudentRegistration.objects.get(sub_student_email_address = serializer.data['student_user_email']).id)
                    try:
                        form = StudentDeviceReg(user=request.user, student_admin_id = student_admin_id, device_name=student_device_name, device_serial_number = student_device_serial_number, 
                        device_os = student_device_os, student_user_id = SubStudentID, student_device_health = student_device_health,
                        )
                        form.save()
                        return Response({
                            "status": status.HTTP_200_OK,
                            "message": "Device registered successfully.",
                            "data": serializer.data
                        })                    
                    except:
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "An error ocured, please try again"
                        })                    
                else:
                    return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "An error ocured, sub student is not under your jurisdiction"
                })            
            else:
                return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message': 'Submission error, kindly try again',
                    'error': serializer.error_messages
                })            
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured and device could not be registered. Kindly try again and provide all required details",
        }) 



@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['post'], request_body=SubStudentRegistrationSerializer)
@csrf_exempt
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
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
                StudentAdminID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
                StudentAdminData = StudentDHMSSignUp.objects.get(student_email = request.user.email)
                StudentAdminEmail = StudentAdminData.student_email
                StudentAdminFirstName = StudentAdminData.student_firstname
                sub_student_firstname = serializer.data['sub_student_firstname']
                sub_student_lastname = serializer.data['sub_student_lastname']
                sub_student_email_address = serializer.data['sub_student_email_address']
                sub_student_phone_number = serializer.data['sub_student_phone_number']
                sub_student_school_name = serializer.data['sub_student_school_name']
                sub_student_matric_number = serializer.data['sub_student_matric_number']

                checkEmailExit = SubStudentRegistration.objects.filter(sub_student_email_address = sub_student_email_address)
                checkEmailExitInUser = User.objects.filter(email = sub_student_email_address)
                checkEmailOfAdminStudent = StudentDHMSSignUp.objects.get(student_email = StudentAdminEmail).student_email
                # checkEmailOfAdminStudent = StudentDHMSSignUp.objects.get(id = StudentAdminID).student_email
                Sub_Student_UniqueID = 'substudent' + '-' +  get_random_string(length=7)

                if(sub_student_email_address is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing student email address",
                        "error_message": serializer.error_messages
                    })
                if(sub_student_phone_number is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing student phone number",
                        "error_message": serializer.error_messages
                    })
                if(sub_student_school_name is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing student school name",
                        "error_message": serializer.error_messages
                    })
                if(sub_student_matric_number is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing student matric number",
                        "error_message": serializer.error_messages
                    })
                if(sub_student_firstname is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing student firstname",
                        "error_message": serializer.error_messages
                    })
                if(sub_student_lastname is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing student lastname",
                        "error_message": serializer.error_messages
                    })
                if checkEmailExit or checkEmailExitInUser:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Email address allocated to sub student already exist on the DHMS. Kindly use a unique email address",
                    })
                if(checkEmailOfAdminStudent is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "You do not have permission to register a student. You have to be registered as an admin on the student DHMS to do this",
                        "error_message": serializer.error_messages
                    })
                
                try:
                    substudentformreg = SubStudentRegistration(user=request.user, sub_student_firstname = sub_student_firstname, sub_student_lastname = sub_student_lastname, sub_student_email_address=sub_student_email_address, 
                    sub_student_admin_id = StudentAdminID, sub_student_password = Sub_Student_UniqueID, sub_student_phone_number = sub_student_phone_number, sub_student_school_name = sub_student_school_name,
                    sub_student_matric_number = sub_student_matric_number)

                    substudentuserprofilecreation = User.objects.create_user(username = sub_student_email_address, first_name = sub_student_firstname, email = sub_student_email_address, 
                                    last_name = sub_student_lastname, password = Sub_Student_UniqueID)

                    substudentformreg.save()
                    substudentuserprofilecreation.save()
                    try:                    
                        SendSubStudentEmailNotification(request, sub_student_email_address, Sub_Student_UniqueID, StudentAdminEmail, StudentAdminFirstName)
                    
                    except:
                        Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Substudebt notification email was NOT sent successfully"
                        }) 
                    
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Sub Student profile created successfull.",
                        "data": serializer.data
                    })
                
                except:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "An error ocured, please try again"
                    })            
            else:
                return Response({
                    'status':status.HTTP_400_BAD_REQUEST,
                    'message': 'Login Failed, check your login details and try again',
                    'error': serializer.error_messages
                }) 
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "An error ocured, kindly fill the form properly",
                "error": serializer.error_messages
            }) 
    # sub_student_admin_email = request.user.email



@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['PUT'])
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UnassignDevice(request, id):   
    """
    Unassign a device and assign to the student admin who registered the device
    """
    try:
        # if request.method == 'POST':
        if id:
            checkStudentExist = StudentDeviceReg.objects.get(id = id)
            device_admin_id = StudentDeviceReg.objects.get(id = id).student_admin_id
            # device_admin_email = User.objects.get(id = device_admin_id).email
            studentAdminID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
            # 
            user_update = {"student_user_id": studentAdminID}
            serializer = UpdateDeviceAssigneeSerializer(checkStudentExist, data = user_update)
            # serializer = UpdateDeviceAssigneeSerializer(checkStudentExist, data = request.user.email)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status":status.HTTP_200_OK,
                    "message": "Device has been unassigned to student and assigned to the student admin",
                    "data": serializer.data 
                })
            else: 
                return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "An error was encountered while trying to unassign this device. Kindly try again",
                    'error': serializer.error_messages
                })
        else:
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid ID. No student matched the ID provided',
            })         
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error ocured, kindly fill the form properly",
        }) 



# GET ALL STUDENT ADMIN REGISTERED DEVICES ENDPOINT
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllStudentDevices(request):
    FoundDevices = []
    try:
        currentAdminID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
        if StudentDeviceReg.objects.filter(student_admin_id = currentAdminID):
            device_admin_email = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_email
            checkDeviceExist = StudentDeviceReg.objects.filter(student_admin_id = currentAdminID)
            if checkDeviceExist.count() > 1:
                for checkDeviceExist in checkDeviceExist:
                    device_name = checkDeviceExist.device_name
                    device_id = checkDeviceExist.id
                    device_serial_number = checkDeviceExist.device_serial_number
                    device_os = checkDeviceExist.device_os
                    device_device_health = checkDeviceExist.student_device_health
                    device_user_id = checkDeviceExist.student_user_id
                    if SubStudentRegistration.objects.filter(id = device_user_id):
                        device_user_email = SubStudentRegistration.objects.get(id = device_user_id).sub_student_email_address
                    elif StudentDHMSSignUp.objects.filter(id = device_user_id):
                        device_user_email = StudentDHMSSignUp.objects.get(id = device_user_id).student_email
                    else:
                        device_user_email = None
                    device_registration_date = checkDeviceExist.created_at              
                    
                    if StudentDHMSSignUp.objects.filter(student_email = device_user_email):
                        fetchUserData = StudentDHMSSignUp.objects.get(student_email = device_user_email)
                        fetchUserFirstName = fetchUserData.student_firstname
                        fetchUserLastName = fetchUserData.student_lastname
                        fetchUserEmail = fetchUserData.student_email
                        fetchUserSchool = fetchUserData.student_school
                        fetchUserPhone = fetchUserData.student_phone
                        fetchUserID = fetchUserData.id

                        fetchUserDataList = {
                            'DeviceUserFirstName':fetchUserFirstName, 'DeviceUserLastName':fetchUserLastName, 
                            'DeviceUserEmail':fetchUserEmail, 'DeviceUserID': fetchUserID,
                            'DeviceUserSchool':fetchUserSchool, 'DeviceUserPhone': fetchUserPhone
                        }
                        
                    elif SubStudentRegistration.objects.filter(sub_student_email_address = device_user_email):
                            fetchUserData = SubStudentRegistration.objects.get(sub_student_email_address = device_user_email)
                            fetchUserFirstName = fetchUserData.sub_student_firstname
                            fetchUserLastName = fetchUserData.sub_student_lastname
                            fetchUserEmail = fetchUserData.sub_student_email_address
                            fetchUserSchool = fetchUserData.sub_student_school_name
                            fetchUserPhone = fetchUserData.sub_student_phone_number
                            fetchUserID = fetchUserData.id

                            fetchUserDataList = {
                                'DeviceUserFirstName':fetchUserFirstName, 'DeviceUserLastName':fetchUserLastName, 'DeviceUserEmail':fetchUserEmail,
                                'DeviceUserSchool':fetchUserSchool, 'DeviceUserPhone': fetchUserPhone, 'DeviceUserID':fetchUserID
                            }
                    else:
                        fetchUserDataList = None
                        
                                            
                    FoundData = {"device_id":device_id, "device_name":device_name, "device_serial_number":  device_serial_number, 'device_os': device_os, 'device_health': device_device_health,
                                'device_user_data':fetchUserDataList, 'device_user_admin': device_admin_email, "device_registration_date":device_registration_date}
                    FoundDevices.append(FoundData)
                return Response({
                    "status":status.HTTP_200_OK,
                    "message": "Student Devices found",
                    "data": FoundDevices,
                    })
            else:
                checkDeviceExist = StudentDeviceReg.objects.get(student_admin_id = currentAdminID)
                device_name = checkDeviceExist.device_name
                device_id = checkDeviceExist.id
                device_serial_number = checkDeviceExist.device_serial_number
                device_os = checkDeviceExist.device_os
                device_device_health = checkDeviceExist.student_device_health
                device_user_id = checkDeviceExist.student_user_id
                if SubStudentRegistration.objects.filter(id = device_user_id):
                    device_user_email = SubStudentRegistration.objects.get(id = device_user_id).sub_student_email_address
                elif StudentDHMSSignUp.objects.filter(id = device_user_id):
                    device_user_email = StudentDHMSSignUp.objects.get(id = device_user_id).student_email
                else:
                    device_user_email = None
                device_registration_date = checkDeviceExist.created_at
                
                # get device user data starts here
                if StudentDHMSSignUp.objects.filter(student_email = device_user_email):
                    currentAdminUser = StudentDHMSSignUp.objects.get(student_email = device_user_email)                    
                    
                    fetchUserFirstName = currentAdminUser.student_firstname
                    fetchUserLastName = currentAdminUser.student_lastname
                    fetchUserEmail = currentAdminUser.student_email
                    fetchUserSchool = currentAdminUser.student_school
                    fetchUserPhone = currentAdminUser.student_phone   
                    fetchUserID = currentAdminUser.id                 

                    fetchUserDataList = {
                        'DeviceUserFirstName':fetchUserFirstName, 'DeviceUserLastName':fetchUserLastName, 'DeviceUserEmail':fetchUserEmail,
                        'DeviceUserSchool':fetchUserSchool, 'DeviceUserPhone': fetchUserPhone, 'DeviceUserID': fetchUserID,
                    }
                    
                elif SubStudentRegistration.objects.filter(sub_student_email_address = device_user_email):
                    currentDeviceUser = SubStudentRegistration.objects.get(sub_student_email_address = device_user_email)
                    
                    fetchUserFirstName = currentDeviceUser.sub_student_firstname
                    fetchUserLastName = currentDeviceUser.sub_student_lastname
                    fetchUserEmail = currentDeviceUser.sub_student_email_address
                    fetchUserSchool = currentDeviceUser.sub_student_school_name
                    fetchUserPhone = currentDeviceUser.sub_student_phone_number
                    fetchUserMatricNumber = currentDeviceUser.sub_student_matric_number   
                    fetchUserID = currentDeviceUser.id                   
                    
                    fetchUserDataList = {
                        'DeviceUserID': fetchUserID, 'DeviceUserFirstName':fetchUserFirstName, 'DeviceUserLastName':fetchUserLastName, 'DeviceUserEmail':fetchUserEmail,
                        'DeviceUserSchool':fetchUserSchool, 'DeviceUserPhone': fetchUserPhone, 'deviceUserMatricNumber' : fetchUserMatricNumber
                    }
                
                else:
                    fetchUserDataList = None
                
                # get device data start here
                FoundData = {"device_id":device_id, "device_name":device_name, "device_serial_number":  device_serial_number, 'device_os': device_os, 'device_health': device_device_health,
                            'device_user_data':fetchUserDataList, 'device_user_admin': device_admin_email, "device_registration_date":device_registration_date}
                FoundDevices.append(FoundData)
                # if device_admin_email == device_user_email:        
                return Response({
                    "status":status.HTTP_200_OK,
                    "message": "Student Devices found",
                    "data": FoundDevices,
                    })
            
            # else:
            #     check_user_exit = SubStudentRegistration.objects.get(sub_student_email_address = device_user_email)
            #     device_user_email = check_user_exit.sub_student_email_address
            #     device_user_phone = check_user_exit.sub_student_phone_number
            #     device_user_school = check_user_exit.sub_student_school_name
            #     device_user_id = check_user_exit.id
            #     if checkDeviceExist:
            #         return Response({
            #             "status":status.HTTP_200_OK,
            #             "message": "Student Devices found",
            #             "data": {"device_id":device_id, 'device_user_id':device_user_id, "device_serial_number":  device_serial_number, 'device_os': device_os, 'device_health': device_device_health,
            #                     'device_user_email':device_user_email, 'device_user_phone':device_user_phone, "device_user_name": device_name,  
            #                     'device_user_school':device_user_school, 'device_registration_date':device_registration_date}
            #             })
                
            #     else:
            #         return Response({
            #         "status": status.HTTP_400_BAD_REQUEST,
            #         "message": "No device is assigned to you."
            #         })
        
        else:
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "No device is assigned to you."
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })



# GET SPECIFIC STUDENT ADMIN REGISTERED DEVICES ENDPOINT
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetSingleStudentDevices(request, id):
    try:
        if id:
            getAdminID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
            specificDevice = StudentDeviceReg.objects.get(Q(id = id) & Q(student_admin_id = getAdminID))    
            serializer = AllStudentDevicesSerializer(specificDevice, many=False)
            if serializer:
                return Response({
                    "status":status.HTTP_200_OK,
                    "message": "Student Device found",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "No device with specified ID",
                })
        else:
            Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Device with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "You're probably not authenticated. Kindly try again"
        })


# SUPER ADMIN FUNCTIONS STARTS HERE
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['post'], request_body=ItsaSuperAdminLoginSerializer)
@csrf_exempt
@api_view(['POST'])
def ItsaSuperAdminLoginFxn(request):
    # try:
    if request.method == 'POST':   
        serializer = ItsaSuperAdminLoginSerializer(data = request.data)
        # try:
        if serializer.is_valid():
            admin_email = serializer.data['username']
            admin_password = serializer.data['password']
            print('serializer valid')
            

            # Admin student Login setup starts here
            if SuperAdminsModel.objects.filter(email = admin_email).exists():
                CheckAdminUserAvaibility = SuperAdminsModel.objects.filter(email = admin_email)
                                    
                token_serializer = CustomTokenObtainPairSerializer(data=request.data)
                token_serializer.is_valid(raise_exception=True)

                # All student Login setup starts here
                CheckUserModelAvaibility = User.objects.get(email = admin_email)
                CheckUserUsername = User.objects.get(email = admin_email).username
                    
                if CheckAdminUserAvaibility is None:
                    return Response({
                        'status':status.HTTP_400_BAD_REQUEST,
                        'message': 'Email and password do not match, Try again',
                        'error': serializer.error_messages
                    })
                if CheckUserModelAvaibility is None:
                    return Response({
                        'status':status.HTTP_400_BAD_REQUEST,
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
                    LatestRegisteredCompanyName = SignupForm.objects.all()[1:2].values_list('companyname', flat=True)[0]
                    AllLatestRegisteredCompanyDevices = DeviceRegisterUpload.objects.filter(CompanyUniqueCode = LatestRegisteredCompanyID)
                    LatestRegCompDevices = AllLatestRegisteredCompanyDevices.count()
                    LatestRegCompFaultyDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Faulty') & Q(CompanyUniqueCode = LatestRegisteredCompanyID))
                    LatestRegCompFaultyDevicesCount = LatestRegCompFaultyDevices.count()
                    LatestRegCompWorkingDevices = DeviceRegisterUpload.objects.filter(Q(devicestatus = 'Working') & Q(CompanyUniqueCode = LatestRegisteredCompanyID))
                    LatestRegCompWorkingDevicesCount = LatestRegCompWorkingDevices.count()
                    LatestRegCompStaff = StaffDataSet.objects.filter(CompanyUniqueCode = LatestRegisteredCompanyID)
                    LatestRegCompStaffCount = LatestRegCompStaff.count()
                    print('LatestRegisteredCompanyID')
                    
                if admin_user is not None:
                    login(request, admin_user)
                    session_id = request.session.session_key
                    return Response({
                        'status':status.HTTP_200_OK,
                        'message': 'Admin Login was Successfull',
                        "Token": token_serializer.validated_data,
                        "studentData": {"email": Admin_email, "adminName":  Admin_name, 'NumberofOrg': AllCompanyCount, 'NumberofDevices': AllDevicesCount,
                                        'NumberofFaultyDevices':AllFaultyDevicesCount, 'NumberofHealthyDevices':AllHealthyDevicesCount, 'LatestRegCompDevices':LatestRegCompDevices,
                                        'LatestRegCompName':LatestRegisteredCompanyName, 'LatestRegCompFaultyDevicesCount':LatestRegCompFaultyDevicesCount, 'LatestRegCompWorkingDevicesCount':LatestRegCompWorkingDevicesCount,
                                        'LatestRegCompStaffCount':LatestRegCompStaffCount},
                    })
                    
                    
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "An error occured",
                    "error_message": "You have to be the super admin to gain access"
                })
                    
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "An error occured",
                "error_message": serializer.error_messages
            })
    else:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured",
            "error_message": "REQUEST FORMAT NOT ACCEPTED"
        })
    # except:
    #     return Response({
    #         "status": status.HTTP_400_BAD_REQUEST,
    #         "message": "An error occured",
    #         "error_message": 'An error occured while processing your request'
    #     })



@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllRegStudents(request):
    FoundStudents = []
    try:
        studentAdminID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
        if SubStudentRegistration.objects.filter(sub_student_admin_id = studentAdminID):
            currentUserStudents = SubStudentRegistration.objects.filter(sub_student_admin_id = studentAdminID)
            if currentUserStudents.count() > 1:
                for currentUserStudents in currentUserStudents:            
                    sub_student_id = currentUserStudents.id
                    sub_student_firstname = currentUserStudents.sub_student_firstname
                    sub_student_lastname = currentUserStudents.sub_student_lastname
                    sub_student_email_address = currentUserStudents.sub_student_email_address
                    sub_student_phone_number = currentUserStudents.sub_student_phone_number
                    sub_student_school_name = currentUserStudents.sub_student_school_name
                    sub_student_matric_number = currentUserStudents.sub_student_matric_number
                    created_at = currentUserStudents.created_at
                    
                    FoundStudentsData = {
                        "sub_student_id":sub_student_id, "sub_student_firstname":sub_student_firstname, "sub_student_lastname":sub_student_lastname, "sub_student_email_address":sub_student_email_address,
                        "sub_student_phone_number":sub_student_phone_number, "sub_student_school_name":sub_student_school_name, "sub_student_matric_number":sub_student_matric_number,
                        "date_registered":created_at
                    }
                    FoundStudents.append(FoundStudentsData)            
                    
                return Response({
                    "status":status.HTTP_200_OK,
                    "message": "Students found",
                    "data": FoundStudents
                })
            else:
                currentUserStudents = SubStudentRegistration.objects.get(sub_student_admin_id = studentAdminID)
                sub_student_firstname = currentUserStudents.sub_student_firstname
                sub_student_lastname = currentUserStudents.sub_student_lastname
                sub_student_email_address = currentUserStudents.sub_student_email_address
                sub_student_phone_number = currentUserStudents.sub_student_phone_number
                sub_student_school_name = currentUserStudents.sub_student_school_name
                sub_student_matric_number = currentUserStudents.sub_student_matric_number       
                sub_student_id = currentUserStudents.id
                created_at = currentUserStudents.created_at
                    
                FoundStudentsData = {
                    "sub_student_id":sub_student_id,"sub_student_firstname":sub_student_firstname, "sub_student_lastname":sub_student_lastname, "sub_student_email_address":sub_student_email_address,
                    "sub_student_phone_number":sub_student_phone_number, "sub_student_school_name":sub_student_school_name, "sub_student_matric_number":sub_student_matric_number,
                    "date_registered":created_at
                }
                
                FoundStudents.append(FoundStudentsData)            
                
                return Response({
                    "status":status.HTTP_200_OK,
                    "message": "Students found",
                    "data": FoundStudents
                })
        else:
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "You have not registered any students yet."
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })


# GET SPECIFIC STUDENT ADMIN REGISTERED DEVICES ENDPOINT
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetSingleStudents(request, id):
    try:
        if id:
            currentLoggedInUserID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
            specificStudent = SubStudentRegistration.objects.get(Q(id = id) & Q(sub_student_admin_id = currentLoggedInUserID))
            serializer = FetchStudentSerializer(specificStudent, many=False)
            if serializer:
                return Response({
                    "status":status.HTTP_200_OK,
                    "message": "Student found",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "No student with specified ID",
                })
        else:
            Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Student with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Student could not be found. Kindly try again"
        })



@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['PUT'], request_body=FetchStudentSerializerForEdit)
@permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['PUT'])
def EditStudentData(request, id):
    try:
        if id:
            currentLoggedInUserID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
            specificStudent = SubStudentRegistration.objects.get(Q(id = id) & Q(sub_student_admin_id = currentLoggedInUserID))
            serializer = FetchStudentSerializerForEdit(specificStudent, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status":status.HTTP_200_OK,
                    "message": "Student info updated",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "An error occured while trying to save updates, kindly try again",
                })
        else:
            Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Student with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. If you want, you can try again"
        })



@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['DELETE'])
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteStudentData(request, id):
    try:
        if id:
            currentLoggedInUserID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
            DeviceStudent = SubStudentRegistration.objects.get(Q(id = id) & Q(sub_student_admin_id = currentLoggedInUserID))
            if DeviceStudent:
                DeviceStudent.delete()
                return Response({
                "status": status.HTTP_200_OK,
                "message": "Student was deleted successfully."
                })
            else:
                return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Student with specified ID was not found under your directory."
                })
        else:
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Student with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. If you want, you can try again"
        })
    


@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['PUT'], request_body=DeviceSerializerForEdit)
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def EditDeviceData(request, id):
    try:
        if id:
            currentLoggedInUserID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
            DeviceStudent = StudentDeviceReg.objects.get(Q(id = id) & Q(student_admin_id = currentLoggedInUserID))
            serializer = DeviceSerializerForEdit(DeviceStudent, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status":status.HTTP_200_OK,
                    "message": "Device info updated",
                    "data": serializer.data
                })
            else: 
                return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "An error occured while trying to save updates, kindly try again",
                })
        else:
            Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Device with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. If you want, you can try again"
        })


@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['DELETE'])
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteDeviceData(request, id):
    try:
        if id:
            currentLoggedInUserID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
            DeviceStudent = StudentDeviceReg.objects.get(Q(id = id) & Q(student_admin_id = currentLoggedInUserID))
            DeviceStudent.delete()
            return Response({
            "status": status.HTTP_200_OK,
            "message": "Device was deleted successfully."
            })
        else:
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Device with specified ID was not found under your directory."
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. If you want, you can try again"
        })
    


# @swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['PUT'])
# @csrf_exempt
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def EditDeviceData(request, id):
#     try:
#         if id:
            # currentLoggedInUserID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
#             DeviceStudent = StudentDeviceReg.objects.get(Q(id = id) & Q(student_admin_id = currentLoggedInUserID))
#             DeviceStudent.delete()
#             return Response({
#             "status": status.HTTP_200_OK,
#             "message": "Device was deleted successfully."
#             })
#         else:
#             return Response({
#             "status": status.HTTP_400_BAD_REQUEST,
#             "message": "Device with specified ID was not found under your directory."
#             })
#     except:
#         return Response({
#             "status": status.HTTP_400_BAD_REQUEST,
#             "message": "An error occured. If you want, you can try again"
#         })



@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
            "status":status.HTTP_200_OK,
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
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured trying to find maintenance requests records"
        })


@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['post'], request_body=MaintenanceRequestSerializer)
@csrf_exempt
@api_view(['POST'])
def MaintenanceReg(request):
    try:
        if request.method == 'POST':
            today = date.today()
            serializer = MaintenanceRequestSerializer(data = request.data)
            if serializer.is_valid():
                # 'student_requester_id', 'student_admin_id', 
                device_id = serializer.data['device_id']
                # device_name = serializer.data['device_name']
                maintenance_priority_level = serializer.data['maintenance_priority_level']
                maintenance_issue = serializer.data['maintenance_issue']
                maintenance_description = serializer.data['maintenance_description']  
                user = User.objects.get(email = request.user.email)
                registeredMonth = today.strftime("%b")
                print(f'{maintenance_priority_level} {device_id} {maintenance_description}')
                    
                # check device ID
                if (StudentDeviceReg.objects.filter(id = serializer.data['device_id'])):
                    # check if student admin is the requester
                    device_name = StudentDeviceReg.objects.get(id = serializer.data['device_id']).device_name
                    if StudentDHMSSignUp.objects.filter(student_email = request.user.email):
                        signedInAdminID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id 
                        print(StudentDeviceReg.objects.get(id = serializer.data['device_id']).student_admin_id)           
                        if int(signedInAdminID) == int(StudentDeviceReg.objects.get(id = serializer.data['device_id']).student_admin_id):
                        # deviceAdminID = StudentDeviceReg.objects.get(id = serializer.data['device_id']).student_admin_id                            
                            # signedInAdminEmail = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_email                            
                            if signedInAdminID:
                                form = StudentMaintenanceRequest(user = user, student_requester_id= signedInAdminID, student_admin_id = signedInAdminID,
                                device_id = device_id, device_name=device_name, maintenance_priority_level = maintenance_priority_level, student_requester_status = 'StudentAdmin',
                                maintenance_issue = maintenance_issue,  maintenance_description = maintenance_description, registeredMonth = registeredMonth)
                                form.save()
                                return Response({
                                    "status": status.HTTP_200_OK,
                                    "message": "Maintenance request placed successfully by the admin"
                                })
                        else:
                            return Response({
                                "status": status.HTTP_200_OK,
                                "message": "This device is not under your jurisdiction"
                            })
                            
                    elif SubStudentRegistration.objects.filter(sub_student_email_address = request.user.email):
                        # 
                        deviceUserID = StudentDeviceReg.objects.get(id = serializer.data['device_id']).student_user_id
                        signedInSubStudentID = SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).id
                        # 
                        if int(signedInSubStudentID) == int(deviceUserID):
                            form = StudentMaintenanceRequest(user = user, student_requester_id= signedInSubStudentID, device_name=device_name, 
                            maintenance_priority_level = maintenance_priority_level, student_admin_id = signedInAdminID, registeredMonth = registeredMonth,
                            maintenance_issue = maintenance_issue,  maintenance_description = maintenance_description, device_id = device_id,
                            student_requester_status = 'SubStudent',
                            )  
                            form.save()
                            return Response({
                                "status": status.HTTP_200_OK,
                                "message": "Maintenance request placed successfully for sub student"
                            })
                        else:
                            return Response({
                                "status": status.HTTP_400_BAD_REQUEST,
                                "message": "You are not authorized to request a maintenance for this device."
                            })            
                    else:
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "An error occured while trying to submit your maintenance request. Kindly confirm your authentication and try again"
                        })            
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "The device ID you submitted is not valid"
                    })            
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Please the data you provided is invalid. Please try again"
                })            
        else:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Welcome to the endpoint for maintenance request. Please submit required details to request for maintenance"
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })


@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FetchMaintenaceRequests(request):
    try:
        AdminLoggedInUserID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
        print(AdminLoggedInUserID)
        if StudentMaintenanceRequest.objects.filter(student_admin_id = AdminLoggedInUserID):
            getAllMaintenanceRequests = StudentMaintenanceRequest.objects.filter(student_admin_id = AdminLoggedInUserID)
            serializer = FetchAllMaintenanceRequestsSerializer(getAllMaintenanceRequests, many=True)
            if serializer:
                return Response({
                    "status":status.HTTP_200_OK,
                    "message": "Maintenance request found",
                    "data": serializer.data
                })
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "We experienced an error while trying to fetch maintenance requests"
                })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "You have no maintenance request yet."
            })            
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured."
        })


@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetEmailValidationCode(request):
    try:
        if request.method == 'GET':
            #  SETUP TO SEND CODE FOR ADMIN STUDENT STARTS HERE
            if StudentDHMSSignUp.objects.filter(student_email = request.user.email):
                StudentEmailAddress = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_email
                user_update = {"email": StudentEmailAddress}
                serializer = GetEmailAddress(data = user_update)
                if serializer.is_valid():
                    LoggedInAdminEmailAddress = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_email
                    LoggedInAdminName = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_firstname
                    recipient_list = [LoggedInAdminEmailAddress]
                    # SETUP EMAIL SENDING FUNCTIONALITY
                    email_address = LoggedInAdminEmailAddress
                    otp = generate_validation_code(request, email_address)
                    if otp == 'CODE SENT':
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": f'Max code request reached, try to login again after about 10 minutes'
                        })
                    elif otp == 'CODE EXPIRED':
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": 'Code expired. Kindly request for a new code'
                        })
                    
                    else:
                        context = {'userName':LoggedInAdminName, 'otp':otp, 'emailAddress':LoggedInAdminEmailAddress}
                        html_message = render_to_string("mailouts/emailvalidationmail.html", context=context)
                        plain_message = strip_tags(html_message)

                        message = EmailMultiAlternatives(
                            subject = "Your DHMS Verification Code", 
                            body = plain_message,
                            from_email = 'dhmsinventoryapp@gmail.com',
                            to= recipient_list
                            )        
                        
                        message.attach_alternative(html_message, "text/html")
                        message.send()

                        if message:
                            print('Sent a OTP code via email')
                            return Response({
                                "status":status.HTTP_200_OK,
                                "message": f"Validation email has been sent successfully to {LoggedInAdminEmailAddress}",
                            })
                        else:
                            return Response({
                                "status": status.HTTP_400_BAD_REQUEST,
                                "message": f'Problem sending OTP code via email to {LoggedInAdminEmailAddress}, check if you typed it correctly'
                            })
                        # else:
                        #     return Response({
                        #         "status": status.HTTP_400_BAD_REQUEST,
                        #         "message": "Email validation not sent. Kindly check you network and try again"
                        #     })
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Email validation not sent. Kindly check you network and try again"
                    })   
            
            
            #  SETUP TO SEND CODE FOR SUB STUDENT STARTS HERE
            elif SubStudentRegistration.objects.filter(sub_student_email_address = request.user.email):
                StudentEmailAddress = SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).sub_student_email_address
                user_update = {"email": StudentEmailAddress}
                serializer = GetEmailAddress(data = user_update)
                if serializer.is_valid():
                    LoggedInSubStudentEmailAddress = SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).sub_student_email_address
                    LoggedInSubStudentName = SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).sub_student_firstname
                    recipient_list = [LoggedInSubStudentEmailAddress]
                    # SETUP EMAIL SENDING FUNCTIONALITY
                    email_address = LoggedInSubStudentEmailAddress
                    otp = generate_validation_code(request, email_address)
                    if otp == 'CODE SENT':
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": f'Max code request reached, try to login again after about 10 minutes'
                        })
                    elif otp == 'CODE EXPIRED':
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": 'Code expired. Kindly request for a new code'
                        })
                    
                    else:
                        context = {'userName':LoggedInSubStudentName, 'otp':otp, 'emailAddress':LoggedInSubStudentEmailAddress}
                        html_message = render_to_string("mailouts/emailvalidationmail.html", context=context)
                        plain_message = strip_tags(html_message)

                        message = EmailMultiAlternatives(
                            subject = "Your DHMS Verification Code", 
                            body = plain_message,
                            from_email = 'dhmsinventoryapp@gmail.com',
                            to= recipient_list
                            )        
                        
                        message.attach_alternative(html_message, "text/html")
                        message.send()

                        if message:
                            print('Sent a OTP code via email')
                            return Response({
                                "status":status.HTTP_200_OK,
                                "message": f"Validation email has been sent successfully to {LoggedInSubStudentEmailAddress}",
                            })
                        else:
                            return Response({
                                "status": status.HTTP_400_BAD_REQUEST,
                                "message": f'Problem sending OTP code via email to {LoggedInSubStudentEmailAddress}, check if you typed it correctly'
                            })
                        # else:
                        #     return Response({
                        #         "status": status.HTTP_400_BAD_REQUEST,
                        #         "message": "Email validation not sent. Kindly check you network and try again"
                        #     })
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Email validation not sent. Kindly check you network and try again"
                    })   
                    
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "You are not a student admin."
                })   
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Email validation not sent. Kindly check you network and try again"
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured."
        })


@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetPhoneNumberValidationCode(request):
    try:
        if request.method == 'GET':
            if VerifyPhoneNumber.objects.filter(studentID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id):
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Your phone number has already been verified"
                })
            
            else:
                if StudentDHMSSignUp.objects.filter(student_email = request.user.email):
                    StudentPhoneNumber = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_phone
                    user_update = {"phone": StudentPhoneNumber}
                    serializer = GetPhoneNumber(data = user_update)
                    if serializer.is_valid():
                        LoggedInAdminPhoneNumber = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_phone
                        LoggedInAdminName = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_firstname
                        recipient_list = [LoggedInAdminPhoneNumber]
                        # SETUP EMAIL SENDING FUNCTIONALITY
                        phoneNumber = LoggedInAdminPhoneNumber
                        otp = generate_validation_code(request, phoneNumber)
                        if otp == 'CODE SENT':
                            return Response({
                                "status": status.HTTP_400_BAD_REQUEST,
                                "message": f'Max code request reached, try to login again after about 10 minutes'
                            })
                        elif otp == 'CODE EXPIRED':
                            return Response({
                                "status": status.HTTP_400_BAD_REQUEST,
                                "message": 'Code expired. Kindly request for a new code'
                            })
                        
                        else:
                            SendPhoneVerificationCode(LoggedInAdminName, LoggedInAdminPhoneNumber, otp)
                            return Response({
                                "status": status.HTTP_200_OK,
                                "message": f'Verification code has been sent to {LoggedInAdminPhoneNumber}'
                            })   
                    else:
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Verification code not sent. Kindly check you network and try again"
                        })   
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "You are not a student admin."
                    })   
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Verification code not sent. Kindly check you network and try again"
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured."
        })



@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['POST'], request_body=GetValidationCode)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ValidateEmailCode(request):
    try:
        if request.method == 'POST':
            serializer = GetValidationCode(data = request.data)
            if serializer.is_valid():
                # VALIDATE CODE FOR ADMIN STUDENT
                if StudentDHMSSignUp.objects.filter(student_email = request.user.email):
                    StudentEmailAddress = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_email
                    code = serializer.data['code']
                    ValidationStatus = Verify_otp(StudentEmailAddress, code)
                    if ValidationStatus == 'CODE EXPIRED':
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Code expired. Kindly try again"
                        })
                    elif ValidationStatus == 'CODE INVALID':
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Code invalid. Kindly provide the correct code"
                        })
                    elif ValidationStatus == 'CODE VALIDATED':
                        student_admin_id = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
                        if VerifyEmailAddress.objects.filter(studentID = student_admin_id):
                            pass
                        else:
                            student_admin_id = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
                            user = User.objects.get(email =  request.user.email)
                            VerifyEmailAddress.objects.create(user = user, studentID = student_admin_id)
                        return Response({
                            "status": status.HTTP_200_OK,
                            "message": "Code validated for admin student!"
                        })
                        
                       
                # VALIDATE CODE FOR SUB STUDENT
                if SubStudentRegistration.objects.filter(sub_student_email_address = request.user.email):
                    StudentEmailAddress = SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).sub_student_email_address
                    code = serializer.data['code']
                    ValidationStatus = Verify_otp(StudentEmailAddress, code)
                    if ValidationStatus == 'CODE EXPIRED':
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Code expired. Kindly try again"
                        })
                    elif ValidationStatus == 'CODE INVALID':
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Code invalid. Kindly provide the correct code"
                        })
                    elif ValidationStatus == 'CODE VALIDATED':
                        substudent_id = SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).id
                        if VerifyEmailAddress.objects.filter(studentID = substudent_id):
                            pass
                        else:
                            substudent_id = SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).id
                            user = User.objects.get(email =  request.user.email)
                            VerifyEmailAddress.objects.create(user = user, studentID = substudent_id)
                        return Response({
                            "status": status.HTTP_200_OK,
                            "message": "Code validated for substudent!"
                        })
                        
                        
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "You are not an admin student. Kindly login as an admin to validate code"
                    })
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Error occured. Kindly try again"
                })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured."
        })


@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['POST'], request_body=GetValidationCode)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ValidatePhoneCode(request):
    try:
        if request.method == 'POST':
            serializer = GetValidationCode(data = request.data)
            if serializer.is_valid():
                student_admin_id = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
                if StudentDHMSSignUp.objects.filter(student_email = request.user.email):
                    StudentEmailAddress = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_phone
                    code = serializer.data['code']
                    ValidationStatus = Verify_otp(StudentEmailAddress, code)
                    if ValidationStatus == 'CODE EXPIRED':
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Code expired. Kindly try again"
                        })
                    elif ValidationStatus == 'CODE INVALID':
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Code invalid. Kindly provide the correct code"
                        })
                    elif ValidationStatus == 'CODE VALIDATED':
                        if VerifyPhoneNumber.objects.filter(studentID = student_admin_id):
                            pass
                        else:
                            user = User.objects.get(email =  request.user.email)
                            VerifyPhoneNumber.objects.create(user = user, studentID = student_admin_id)
                        return Response({
                            "status": status.HTTP_200_OK,
                            "message": "Code VALIDATED!"
                        })
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "You are not an admin student. Kindly login as an admin to validate code"
                    })
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Error occured. Kindly try again"
                })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Code Validation Failed. Kindly try again"
        })



@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['post'], request_body=StudentTransactionPINSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateTransactionPIN(request):
    try:
        user = User.objects.get(email = request.user.email)
        if request.method == 'POST':
            serializer = StudentTransactionPINSerializer(data = request.data)
            if serializer.is_valid():
                student_pin = serializer.data['student_transaction_pin']
                
                # Execute for admin student
                if StudentDHMSSignUp.objects.filter(student_email = request.user.email):
                    FindStudentID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
                    if StudentTransactionPIN.objects.filter(student_id = FindStudentID):
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Sorry, you have an existing transaction PIN"
                        })
                    
                    adminStudentEmail = StudentDHMSSignUp.objects.get(student_email = request.user.email).student_email
                    
                    form = StudentTransactionPIN(user = user, student_id= FindStudentID, student_transaction_pin = student_pin)  
                    form.save()
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": f'Transaction PIN created successfully for admin: {adminStudentEmail}',
                        "data": {
                            "User_email_address": adminStudentEmail,
                            "User_id": FindStudentID,
                            "New_transaction_pin": student_pin,
                        }
                    })
                
                # Execute for sub student
                elif SubStudentRegistration.objects.filter(sub_student_email_address = request.user.email):
                    FindStudentID = SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).id
                    if StudentTransactionPIN.objects.filter(student_id = FindStudentID):
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Sorry, you have an existing transaction PIN"
                        })
                        
                    subStudentID = SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).id    
                    form = StudentTransactionPIN(user = user, student_id= subStudentID, student_transaction_pin=student_pin)
                    form.save()
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Transaction PIN created successfully for substudent"
                    })  
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "User does not exit"
                    })
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "An error occured. Kindly try again"
                })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Error in request format"
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured"
        })


@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['PUT'], request_body=UpdateStudentTransactionPINSerializer)
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def UpdateTransactionPIN(request):
    # UpdateStudentTransactionPINSerializer
    try:
        serializer = UpdateStudentTransactionPINSerializer(data = request.data)
        if serializer.is_valid():
            oldPIN = serializer.data['oldPin']
            newPIN = serializer.data['newPin']
            
            fetchStudent = StudentTransactionPIN.objects.get(student_email_address = request.user.email)
            fetchPIN = fetchStudent.student_transaction_pin
            if fetchPIN != oldPIN:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "The old PIN is incorrect"
                })
            elif fetchPIN == newPIN:
                return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "Invalid PIN. You have used this PIN before, Kindly use a different PIN",
                })
            elif fetchPIN == oldPIN: 
                # UPDATE PIN HERE
                newPIN = serializer.data['newPin']        
                
                # fetchUserEmailAddress = fetchStudent.student_email_address
                # fetchUserID = fetchStudent.id
                # fetchDataToUse = {"student_email_address": fetchUserEmailAddress, 'student_id': fetchUserID, 'student_transaction_pin': newPIN}
                fetchDataToUse = {'student_transaction_pin': newPIN}
                    
                serializer = FetchStudentTransactionPINSerializerForEdit(fetchStudent, data = fetchDataToUse)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "status":status.HTTP_200_OK,
                        "message": "Transaction PIN updated",
                        "data": serializer.data
                    })
                else: 
                    return Response({
                        "status":status.HTTP_400_BAD_REQUEST,
                        "message": "An error occured while trying to save updates, kindly try again",
                    })        
        else: 
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "An error occured while trying to save updates, kindly try again",
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Please try again"
        })



# CREATE PAYSTACK CUSTOMER
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CreatePaystackCustomer(request):
    try:
        student_admin_id = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
        if RegisterPaystackCustomers.objects.filter(StudentID = student_admin_id):
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'You have registered as a transaction customer already'
            })
        else:            
            getRequestingUser = StudentDHMSSignUp.objects.get(student_email = request.user.email)
            user_EmailAddress = getRequestingUser.student_email
            user_FirstName = getRequestingUser.student_firstname
            user_LastName = getRequestingUser.student_lastname
            user_phone = getRequestingUser.student_phone
            
            url = "https://api.paystack.co/customer"
            headers = {
                'Authorization': f'Bearer {paystackSecretKey}',
                'Content-Type': 'application/json'
            }
            
            data={ 
                "email": user_EmailAddress,
                "first_name": user_FirstName,
                "last_name": user_LastName,
                "phone": user_phone,
                #   "middle_name": user_firstname,
                #   "phone": '+23481000000021',
                #   "bvn": "121212121212",
                #   "preferred_bank": "wema-bank",
                #   "country": "NG"
            }
            
            response = requests.post(url, json=data, headers=headers)
            CustomerSetupResponse = response.json()
            if CustomerSetupResponse['status'] == True:
                RegisterPaystackCustomers.objects.create(
                    StudentID = student_admin_id,
                    # StudentEmailAddress = CustomerSetupResponse['data']['email'],
                    customerCode = CustomerSetupResponse['data']['customer_code'],
                    integration = CustomerSetupResponse['data']['integration'],
                )
                return Response({
                        "status":status.HTTP_200_OK,
                        "message": "Process completed",
                        "data": response.json(),
                    })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured'
        })




# FETCH PAYSTACK CUSTOMER
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FindPaystackCustomer(request):
    try:
        getRequestingUser = StudentDHMSSignUp.objects.get(student_email = request.user.email)
        user_EmailAddress = getRequestingUser.student_email
        
        url=f'https://api.paystack.co/customer/{user_EmailAddress}'
        
        headers = {
            'Authorization': f'Bearer {paystackSecretKey}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return Response({
                "status":status.HTTP_200_OK,
                "message": "Customer details found",
                "data": response.json(),
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Please try again"
        })



# CREATE RECIPIENT CODE FOR EACH USER ON CREATION OF WALLET

def create_transfer_recipient(request, bank_account_name, studentBankCode, bank_account_number):    
    try:
        StudentID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id        
        if StudentTransferRecipientCode.objects.filter(student_id = StudentID):
            pass
        else:
            url = f'https://api.paystack.co/transferrecipient'    
            headers = {
                'Authorization': f'Bearer {paystackSecretKey}',
                'Content-Type': 'application/json',
            }
            
            data = {
                'type': 'nuban',  # 'nuban' is the account type for Nigerian bank accounts
                'name': bank_account_name,
                'bank_code': studentBankCode,
                'account_number': bank_account_number,
                'currency': 'NGN'
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            data = response.json() 
            recipient_id = data['data']['id']
            # recipient_integrations = data['data']['integration']
            recipient_code = data['data']['recipient_code']
            bank_code = data['data']['details']['bank_code']
            bank_account_number = data['data']['details']['account_number']
            # user = User.objects.get(email =  request.user.email)
            print('datadata')
            print(StudentID)
            print(data)

            saveDataToDB = {'recipient_id':recipient_id, 'recipient_code':recipient_code, 
                            'bank_customer_code':bank_code, 'student_id': StudentID, 'bank_account_number': bank_account_number
                            }
            serializer = SavePayStackRecipientIDSerializer(data = saveDataToDB)
            if serializer.is_valid():
                StudentTransferRecipientCode.objects.create(                    
                    user = request.user,
                    bank_customer_code = bank_code,
                    bank_account_number = bank_account_number,
                    student_id = StudentID,
                    recipient_code = recipient_code,
                    recipient_id = recipient_id,
                )
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'Recipient code created',
                    'data': response.json(),
                    })
            else:
                print('SavePayStackRecipientIDSerializer is NOT VALID')
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Recipient code not created',
                    "error_message": serializer.error_messages
                    })    
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured',
            })

        

# CREATE VIRTUAL ACCOUNT
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CreateDedicatedVirtualAccount(request):
    try:
        StudentID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
        if PayStackCustomerWalletDetails.objects.filter(student_id = StudentID):
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'You have created a dedicated wallet account already.'
            })
                
        else:
            getRequestingUser = StudentDHMSSignUp.objects.get(student_email = request.user.email)
            user_EmailAddress = getRequestingUser.student_email
            
            url= "https://api.paystack.co/dedicated_account"
            
            headers = {
                'Authorization': f'Bearer {paystackSecretKey}',
                'Content-Type': 'application/json'
            }
            
            data={
                "customer": user_EmailAddress, 
                "preferred_bank":"wema-bank"
            }
            if PayStackCustomerWalletDetails.objects.filter(student_id = StudentID):
                # PayStackCustomerWalletDetails.objects.filter(student_email_address = request.user.email).delete()
                pass
            else:
                response = requests.post(url, json=data, headers=headers)
                data = response.json()
                print('data')
                print(data['data']['bank']['name'])
                bank_name = data['data']['bank']['name']
                bank_name_slug = data['data']['bank']['slug']
                bank_account_name = data['data']['account_name']
                bank_account_number = data['data']['account_number']
                bank_account_currency = data['data']['currency']
                bank_account_creation_date = data['data']['created_at']
                bank_customer_code = data['data']['customer']['customer_code']   
                # user = User.objects.get(email =  request.user.email)
                StudentID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
                
                saveBankDataToDB = {'bank_name':bank_name, 'bank_name_slug':bank_name_slug, 'bank_account_name':bank_account_name, 
                                    'bank_account_number':bank_account_number, 'bank_account_currency':bank_account_currency, 
                                    'bank_account_creation_date':bank_account_creation_date, 'bank_customer_code':bank_customer_code,
                                    'student_id': StudentID
                                    }
                
                # CREATE A RECIPIENT ACCOUNT FOR USER STARTS HERE
                studentBankCode = '035'
                recFirstName = data['data']['customer']['first_name']
                recLastName = data['data']['customer']['last_name']
                bank_account_name = f'{recFirstName} {recLastName}'
                create_transfer_recipient(request, bank_account_name, studentBankCode, bank_account_number)
                # CREATE A RECIPIENT ACCOUNT FOR USER ENDS HERE            
                
                serializer = SavePayStackCustomerWalletDetailsSerializer(data = saveBankDataToDB)
                if serializer.is_valid():
                    PayStackCustomerWalletDetails.objects.create(
                        user = request.user,
                        bank_customer_code = bank_customer_code,
                        student_id = StudentID,
                        bank_name = bank_name,
                        bank_name_slug = bank_name_slug,
                        bank_account_name = bank_account_name,
                        bank_account_number = bank_account_number,
                        bank_account_currency = bank_account_currency,
                        bank_account_creation_date = bank_account_creation_date,                        
                    )
                    # serializer.save()
                    return Response({
                            "status":status.HTTP_200_OK,
                            "message": "Dedicated wallet created successfully",
                            "data": response.json(),
                        })
                else:
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Something went wrong with data serialization',
                        'error': serializer.error_messages
                    })    
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured. Kindly check your network and try again.'
        })
    
    # First bank code : 011



# FETCT PAYSTACK SUPPORTED BANKS
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
# @permission_classes([IsAuthenticated])
@csrf_exempt
@api_view(['GET'])
def PaystackListofBanks(request):
    try: 
        url= 'https://api.paystack.co/bank'
        
        headers = {
            'Authorization': f'Bearer {paystackSecretKey}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return Response({
                "status":status.HTTP_200_OK,
                "message": "Supported Banks and bank codes found",
                "data": response.json(),
            })
    except:
        return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "An error occured.Kindly try again",
                "data": response.json(),
            })
    


# FETCT PAYSTACK SUPPORTED BANKS
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['POST'], request_body = ValidatePayStackCustomerSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ValidatePayStackCustomer(request):
    try:        
        serializer = ValidatePayStackCustomerSerializer(data = request.data)
        if serializer.is_valid():
            # account_number = serializer.data['account_number']
            bvn = serializer.data['bvn']
            # bank_code = serializer.data['bank_code']            
            getRequestingUser = StudentDHMSSignUp.objects.get(student_email = request.user.email)
            user_EmailAddress = getRequestingUser.student_email
            user_firstname = getRequestingUser.student_firstname
            user_lastname = getRequestingUser.student_lastname
            # test_code = 'CUS_stkf9l71tug3acu'
            
            url=f'https://api.paystack.co/customer/{user_EmailAddress}/identification'
                
            headers = {
                'Authorization': f'Bearer {paystackSecretKey}',
                'Content-Type': 'application/json'
            }
            
            # TEST WITHOUT ACCOUNT ACCOUNT NUMBER AND BANK CODE
            
            data={
                "country": "NG",
                "type": "bank_account",
                # "account_number": account_number,
                "bvn": bvn,
                # "bank_code": bank_code,
                "first_name": user_firstname,
                "last_name": user_lastname
                }
            
            # data={
            #     "country": "NG",
            #     "type": "bank_account",
            #     "account_number": "0111111111",
            #     "bvn": "222222222221",
            #     "bank_code": "007",
            #     "first_name": "Uchenna",
            #     "last_name": "Okoro"
                # }
            
            response = requests.post(url, json=data, headers=headers)
            data = response.json()

            return Response({
                    "data": data,
                    # "data": response.json(),
                })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured, kindly check your network connection and try again'
        })  


@csrf_exempt
@schema(None)  
@api_view(['POST'])
def PaystackWebhookView(request):
    if request.method == 'POST':
        # Verify the webhook signature
        signature = request.headers.get('X-PAYSTACK-SIGNATURE')
        if not signature:
            print('Paystack Signature missing')
            return Response(
                {'detail': 'Authontication failed'}, 
                status=status.HTTP_400_BAD_REQUEST
                )

        secret = paystackSecretKey.encode()
        expected_signature = hmac.new(secret, request.body, hashlib.sha512).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            return Response(
                {'message': 'Invalid signature'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Process the webhook payload
        print('SIGNATURE IS VALID')
        data = json.loads(request.body)
        # print(data)
        event = data.get('event')

        if event == 'customeridentification.failed':
            # Handle charge success event
            handle_customeridentification_failed(data)
        elif event == 'customeridentification.success':
            # Handle subscription creation event
            handle_customeridentification_success(data)
        elif event == 'charge.success':  # when a DVA receives funds
            handle_dva_funds_received(data)

        return Response({'detail': 'Webhook received'}, status=status.HTTP_200_OK)

    return Response({
            "status":status.HTTP_400_BAD_REQUEST,
            "message": "An error occured in webhook endpoint",
        })
    

def handle_customeridentification_failed(data):
    # Process charge success event
    return Response({
            "status":status.HTTP_200_OK,
            "message": "Customer identification failed",
            "data": data,
        })

def handle_customeridentification_success(data):
    # Process subscription creation event
    return Response({
            "status":status.HTTP_200_OK,
            "message": "Customer identification success",
            "data": data,
        })



def handle_dva_funds_received(data):
    try:
        receiverEmail = data["data"]["customer"]['email']
        transactionAmount = data["data"]["amount"]    
        
        # UPDATE ACCOUNT BALANCE FOR USER STARTS HERE
        if StudentDHMSSignUp.objects.filter(student_email = receiverEmail):
            receiverID = int(StudentDHMSSignUp.objects.get(student_email = receiverEmail).id)
        elif SubStudentRegistration.objects.filter(sub_student_email_address = receiverEmail):
            receiverID = int(SubStudentRegistration.objects.get(sub_student_email_address = receiverEmail).id)    
        else:
            return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "System does not recignize your user ID. Kindly logout and login again, or contact support",
                })
        findStudentReciever = PayStackCustomerWalletDetails.objects.get(student_id=receiverID)
        oldWalletBalance = int(findStudentReciever.accountBalance)
        newTransactionAmount = oldWalletBalance + int(transactionAmount) / 100
        newAccountBalance = {'accountBalance': newTransactionAmount}
        serializer = UpdateWalletBalance(findStudentReciever, data = newAccountBalance)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":status.HTTP_200_OK,
                "message": f'Account balance for {receiverEmail} has been updated to {newTransactionAmount}',
                })
        else:
            return Response({
                    "status":status.HTTP_400_BAD_REQUEST,
                    "message": "An error was experienced with serializing user account update before saving",
                    "error": serializer.error_messages,
                })
            
        # UPDATE ACCOUNT BALANCE FOR USER ENDS HERE

    except:
        print(f"Virtual accountfor user {receiverEmail} not found.")
        return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "An error was experienced with serializing user account update before saving",
            })

        


# FETCT ALL DVAs
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def List_DVAs(request):
    try:           
        url="https://api.paystack.co/dedicated_account"
                
        headers = {
            'Authorization': f'Bearer {paystackSecretKey}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        return Response({
                "data": data,
                # "data": response.json(),
            })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured'
        })




# FETCT USER WALLET DETAILS
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FetchWalletDetails(request):
    try:
        if request.user.is_authenticated:
        # if StudentDHMSSignUp.objects.filter(student_email = request.user.email):
            StudentID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
            if PayStackCustomerWalletDetails.objects.filter(student_id = StudentID):
                fetchUserWalletDetails = PayStackCustomerWalletDetails.objects.get(student_id = StudentID)
                # fetchCustomerRecipientCODE = StudentTransferRecipientCode.objects.get(student_id = StudentID).recipient_code
                serializer = FetchPayStackCustomerWalletDetails(fetchUserWalletDetails, many=False)
                if serializer:
                    return Response({
                            "status": 200,
                            "message": 'Account details found',
                            "data": serializer.data,
                            # "customer_recipient_code": fetchCustomerRecipientCODE
                        })
                else:
                    return Response({
                            "status": 400,
                            "message": 'An error occured. Kindly rey again',
                        })
            else:
                return Response({
                        "status": 400,
                        "message": 'You have not created a wallet yet',
                    })
        else:
            return Response({
                    "status": 400,
                    "message": 'You are not logged in',
                })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured'
        }) 



# FETCT DEVICE STATUS ENUMS
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
def Device_Health_Status(request):
    try:
        deviceStatuses = {'Healthy':'Healthy', 'Faulty':'Faulty', 'Critical':'Critical'}
        serializer = Device_Health_Status_Serializer(data = deviceStatuses)
        if serializer.is_valid():
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Device Health Status Options',
                'data': serializer.data
            })
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'An error occured'
            })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured'
        })

# MaintainanceIssueOption = (
#     ("Screen Repairs", "Screen Repairs"),
#     ("Battery Issues", "Battery Issues"),
#     ("Keyboard Issues", "Keyboard Issues"),
#     ("Motherboard Issues", "Motherboard Issues"),
#     ("Others", "Others"),
# )

# FETCT DEVICE STATUS ENUMS
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
def MaintenanceIssueOptions(request):
    try:
        maintenanceOptions = {'Screen Repairs':'Screen Repairs', 'Battery Issues':'Battery Issues', 'Motherboard Issues': 'Motherboard Issues',
                              'Keyboard Issues':'Keyboard Issues', 'Others':'Others'}
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Maintenance issue options were fetched successfully',
            'data': maintenanceOptions
        })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured'
        })



# TRANSFER FUNDS
# Function to initialize a transfer
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['POST'], request_body = InitializeFundTransferSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# def initialize_transfer(amount, recipient_code, reason='Transfer from dedicated virtual account'):
def initialize_transfer(request):
    try:
        """
        Initializes a transfer to a specified recipient.
        
        :param amount: Amount to transfer in kobo (1 Naira = 100 kobo)
        :param recipient_code: The recipient code for the customer (obtained from Paystack)
        :param reason: A note or reason for the transfer (optional)
        :return: Response from Paystack API
        """
        serializer = InitializeFundTransferSerializer(data = request.data)        
        if serializer.is_valid():
            recipient_code = serializer.data['recipient_code']
            amount = serializer.data['amount']
            reason = serializer.data['reason']
            url = f'https://api.paystack.co/transfer'
            
            headers = {
                'Authorization': f'Bearer {paystackSecretKey}',
                'Content-Type': 'application/json',
            }
            
            data = {
                'source': 'balance',  # 'balance' if transferring from your Paystack balance
                'amount': amount,
                'recipient': recipient_code,
                'reason': reason,
            }
            
            response = requests.post(url, headers=headers, json=data)
            dataResponse = response.json()
            dataResStatus = dataResponse['status']
            dataResMessage = dataResponse['message']
            dataResMessageTwo = dataResponse['meta']['nextStep']
            
            
            if dataResStatus == False:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': f'{dataResMessage}. {dataResMessageTwo}',
                })
            else:
                return Response({
                    'status': status.HTTP_200_OK,
                    'data': response.json(),
                })            
        else:        
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'An error occured',
                "error_message": serializer.error_messages
            })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured'
        })
    
    
# Function to finalize a transfer (if OTP or additional authorization is required)
def finalize_transfer(transfer_code, otp):
    """
    Finalizes a transfer if OTP or authorization is needed.
    
    :param transfer_code: The transfer code received from the initialize_transfer function
    :param otp: The OTP sent to the customer for the transfer
    :return: Response from Paystack API
    """
    url = f'https://api.paystack.co/transfer/finalize_transfer'
    
    headers = {
        'Authorization': f'Bearer {paystackSecretKey}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'transfer_code': transfer_code,
        'otp': otp,
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    return Response({
        'status': status.HTTP_200_OK,
        'data': response.json(),
    })


# paystack customer code: CUS_ufzwn9sughvqskp

@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['POST'], request_body = VerifyUserAccountDetailsSerializer)
@csrf_exempt
@api_view(['POST'])
def VerifyUserAccountDetails(request):
    try:
        serializer = VerifyUserAccountDetailsSerializer(data = request.data)
        if serializer.is_valid():
            account_number = serializer.data['account_number']
            bank_code = serializer.data['bank_code']
            
        url = f'https://api.paystack.co/bank/resolve?account_number={account_number}&bank_code={bank_code}'
        
        headers = {
            'Authorization': f'Bearer {paystackSecretKey}',
            'Content-Type': 'application/json',
        }
        
        response = requests.get(url, headers=headers)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Bank details found',
            'data': response.json(),
            })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured',
            })



def FetchTransactionsForCalc(getUserAccountNumber):
    # account_number = '9308219417'
        # account_number = PayStackCustomerWalletDetails.objects.get(student_email_address = request.user.email).bank_account_number
        url = f'https://api.paystack.co/transaction'    
        
        headers = {
            'Authorization': f'Bearer {paystackSecretKey}',
            # 'Content-Type': 'application/json',
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            transactions = response.json().get('data', [])
            # Filter transactions related to the specific virtual account
            account_transactions = [tx for tx in transactions if tx['metadata']['receiver_account_number'] == getUserAccountNumber]
            print(account_transactions)
            return account_transactions
            # return Response({
            #     'status': status.HTTP_200_OK,
            #     'message': 'Transactions found',
            #     'transactions': account_transactions,
            #     })
        else:
            print("Failed to fetch transactions:", response.json())
            return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured',
            })



@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
def Calculate_balance(request):
    try:
        getRequestingUserID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
        getUserAccountNumber = PayStackCustomerWalletDetails.objects.get(student_id = getRequestingUserID).bank_account_number
        
        transactions = FetchTransactionsForCalc(getUserAccountNumber)
        print('transactions')
        print(transactions)
        
        balance = 0
        
        for tx in transactions:
            if tx['status'] == 'success':
                if tx['gateway_response'] == 'Approved':
                    if tx['metadata']['receiver_account_number'] == getUserAccountNumber:
                        balance += int(tx['amount'])
                    else:
                        balance -= int(tx['amount'])
                    # elif tx['transaction_type'] == 'debit':
                    #     balance -= int(tx['amount'])
                else:
                    return Response({
                            'status': status.HTTP_200_OK,
                            'message': 'Account balance found',
                            'account_balance':  balance / 100,
                            })
        
        return Response({
                'status': status.HTTP_200_OK,
                'message': 'Account balance found',
                'account_balance':  balance / 100,
                })
    except:
            return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured. Kindly try again.',
            })


# CALCULATE ACCOUNT BALANCE BELOW
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FetchAllTransactions(request):    
    FoundTransactions = []
    try:
        ResponseData = fetch_and_save_transactions(request)
        if ResponseData == 'No Transaction found for this user':
                return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "No transaction."
        })
        elif ResponseData == "An error occured while updating transactions history":
                return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "An error occured while updating transactions history"
        })

        if StudentDHMSSignUp.objects.get(student_email = request.user.email).id:
            getRequestingID = int(StudentDHMSSignUp.objects.get(student_email = request.user.email).id)
        elif SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).id:
            getRequestingID = int(SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).id)  
        else:
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. User is not a student admin or a substudent."
            })
        currentTransaction = StudentWalletTransactions.objects.filter(SenderStudentID = getRequestingID)
        if currentTransaction.count() > 1:
            for currentTransaction in currentTransaction:            
                transactionType = currentTransaction.transactionType
                transactionAmount = currentTransaction.transactionAmount
                transactionNarration = currentTransaction.transactionNarration
                transactionCardType = currentTransaction.transactionCardType
                transactionStatus = currentTransaction.transactionStatus
                # when transaction is debit
                receiverAccountNumber = currentTransaction.receiverAccountNumber
                receiverAccountStudentID = currentTransaction.receiverAccountStudentID
                receiverAccountName = currentTransaction.receiverAccountName
                receiverAccountBank = currentTransaction.receiverAccountBank
                # When transaction is credit
                senderAccountNumber = currentTransaction.senderAccountNumber
                senderAccountName = currentTransaction.senderAccountName
                senderAccountBank = currentTransaction.senderAccountBank
                # 
                transactionDateFromPaystack = currentTransaction.transactionDateFromPaystack
                created_at = currentTransaction.created_at
        
                
                FoundTransactionsData = {
                    "transactionAmount":transactionAmount, "transactionType":transactionType, "transactionNarration":transactionNarration,
                    "transactionMethod":transactionCardType, "receiverAccountNumber":receiverAccountNumber, "receiverAccountStudentID":receiverAccountStudentID,
                    "receiverAccountName":receiverAccountName, 'receiverAccountBank':receiverAccountBank, "paystackTransactionDate":transactionDateFromPaystack,
                    'senderAccountNumber':senderAccountNumber, 'senderAccountName': senderAccountName, 'senderAccountBank':senderAccountBank, 'transactionStatus':transactionStatus,
                    "dateSaveInDB": created_at
                }
                FoundTransactions.append(FoundTransactionsData)            
                
            return Response({
                "status":status.HTTP_200_OK,
                "message": "Transactions found",
                "data": FoundTransactions
            })
        else:
            currentTransaction = StudentWalletTransactions.objects.get(SenderStudentID = getRequestingID)
            transactionType = currentTransaction.transactionType
            transactionAmount = currentTransaction.transactionAmount
            transactionNarration = currentTransaction.transactionNarration
            transactionCardType = currentTransaction.transactionCardType
            transactionStatus = currentTransaction.transactionStatus
            # when transaction is debit
            receiverAccountNumber = currentTransaction.receiverAccountNumber
            receiverAccountStudentID = currentTransaction.receiverAccountStudentID
            receiverAccountName = currentTransaction.receiverAccountName
            receiverAccountBank = currentTransaction.receiverAccountBank
            # When transaction is credit
            senderAccountNumber = currentTransaction.senderAccountNumber
            senderAccountName = currentTransaction.senderAccountName
            senderAccountBank = currentTransaction.senderAccountBank
            transactionDateFromPaystack = currentTransaction.transactionDateFromPaystack
            created_at = currentTransaction.created_at
                
            FoundTransactionsData = {
                "transactionAmount":transactionAmount, "transactionType":transactionType, "transactionNarration":transactionNarration,
                "transactionMethod":transactionCardType, "receiverAccountNumber":receiverAccountNumber, "receiverAccountStudentID":receiverAccountStudentID,
                "receiverAccountName":receiverAccountName, 'receiverAccountBank':receiverAccountBank, "paystackTransactionDate":transactionDateFromPaystack,
                'senderAccountNumber':senderAccountNumber, 'senderAccountName': senderAccountName, 'senderAccountBank':senderAccountBank, 'transactionStatus':transactionStatus,
                "dateSaveInDB": created_at
            }
            
            FoundTransactions.append(FoundTransactionsData)            
            
            return Response({
                "status":status.HTTP_200_OK,
                "message": "Transaction found",
                "data": FoundTransactions
            })
        
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "No Transaction Found For This Student"
        })


# UPDATE ALL TRANSACTIONS IN DATABASE
def fetch_and_save_transactions(request):
    getReponse = save_new_transactions(request)
    return getReponse


# CHECK KYC COMPLETON
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
def CheckKYCValidation(request):
    try:
        getRequestingID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id 
        # check email verification status 
        if VerifyEmailAddress.objects.filter(studentID = getRequestingID):
            VerifyEmailAddressStatus = True
        else:
            VerifyEmailAddressStatus = False
        # check phone number verification status
        if VerifyPhoneNumber.objects.filter(studentID = getRequestingID):
            VerifyPhoneNumberStatus = True
        else:
            VerifyPhoneNumberStatus = False
        # check transaction PIN setup status
        if StudentTransactionPIN.objects.filter(student_id = getRequestingID):
            StudentTransactionPINSetUpStatus = True
        else:
            StudentTransactionPINSetUpStatus = False
        # check wallet setup status
        if PayStackCustomerWalletDetails.objects.filter(student_id = getRequestingID):
            walletSetUpStatus = True
        else:
            walletSetUpStatus = False
            
        KYCUpdates = {
            'VerifyEmailAddressStatus':VerifyEmailAddressStatus, 'VerifyPhoneNumberStatus':VerifyPhoneNumberStatus,
            'StudentTransactionPINSetUpStatus':StudentTransactionPINSetUpStatus, 'walletSetUpStatus':walletSetUpStatus
            }
        
        return Response({
                        "status":status.HTTP_200_OK,
                        "message": "KYC Statuses found",
                        "data": KYCUpdates        
                    })    
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })



# PLACE STUDENT TRANSFER REQUEST
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['POST'], request_body = PlaceTransferRequestsSerializer)
@csrf_exempt
@api_view(['POST'])
def StudentPlaceTransferRequest(request):
    try:
        serializer = PlaceTransferRequestsSerializer(data = request.data)
        if serializer.is_valid():
            transferAmount = int(serializer.data['transferAmount']),
            transactionPIN = serializer.data['transactionPIN']
            # Check if sender is a student admin
            if (StudentDHMSSignUp.objects.filter(student_email = request.user.email)):
                GetSenderID = int(StudentDHMSSignUp.objects.get(student_email = request.user.email).id)
                
                fetchSenderProfile = StudentDHMSSignUp.objects.get(student_email = request.user.email)
                fetchSenderPhoneNumber = fetchSenderProfile.student_phone
                senderEmail = fetchSenderProfile.student_email
                senderFirstName = fetchSenderProfile.student_firstname
                senderLastName = fetchSenderProfile.student_lastname
                
                if StudentTransactionPIN.objects.filter(student_id = GetSenderID):
                    GetStudentAdminTransPIN = StudentTransactionPIN.objects.get(student_id = GetSenderID).student_transaction_pin
                    # check if transaction pin is correct
                    if (GetStudentAdminTransPIN == serializer.data['transactionPIN']):
                        pass
                    else:
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Sorry, Your transaction pin is incorrect"
                        })
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Sorry, You have not set a transaction pin yet. Please create a transaction PIN and try again"
                    })
            # carry out if sender is a sub student
            elif (SubStudentRegistration.objects.filter(sub_student_email_address = request.user.email)):
                GetSenderID = int(SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).id)
                
                fetchSenderProfile = SubStudentRegistration.objects.get(sub_student_email_address = request.user.email)
                fetchSenderPhoneNumber = fetchSenderProfile.sub_student_phone_number
                senderEmail = fetchSenderProfile.sub_student_email_address
                senderFirstName = fetchSenderProfile.sub_student_firstname
                senderLastName = fetchSenderProfile.sub_student_lastname
                
                if StudentTransactionPIN.objects.filter(student_id = GetSenderID):
                    GetStudentAdminTransPIN = StudentTransactionPIN.objects.get(student_id = GetSenderID).student_transaction_pin
                    # check if transaction pin is correct
                    if (GetStudentAdminTransPIN == serializer.data['transactionPIN']):
                        pass
                    else:
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Sorry, Your transaction pin is incorrect"
                        })
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Sorry, You have not set a transaction pin yet. Please create a transaction PIN and try again"
                    })
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Sorry, You account status cannot be confirmed at this time. Kindly login and try again."
                })
                
            # check if receiver is a student admin 
            if StudentDHMSSignUp.objects.filter(student_email = serializer.data['receiverEmail']):
                receiverID = int(StudentDHMSSignUp.objects.get(student_email = serializer.data['receiverEmail']).id)
                receiverProfile = StudentDHMSSignUp.objects.get(student_email = request.user.email)
            # check if receiver is a sub student 
            elif SubStudentRegistration.objects.filter(sub_student_email_address = serializer.data['receiverEmail']):
                # getSubStudentReceiverID = int(SubStudentRegistration.objects.get(sub_student_email_address = request.user.email).id)
                # fetchSubStudentReceiverProfile = SubStudentRegistration.objects.get(sub_student_email_address = request.user.email)
                receiverProfileProfile = SubStudentRegistration.objects.get(sub_student_email_address = serializer.data['receiverEmail'])
                receiverID = int(SubStudentRegistration.objects.get(sub_student_email_address = serializer.data['receiverEmail']).id ) 
                # 
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Sorry, the reciever does not have a student DHMS account. Kindly send them an invite to download and register on the DHMS and start receiving funds"
                })
            # Check if receiver has a wallet on DHMS
            if PayStackCustomerWalletDetails.objects.filter(student_id = receiverID):
                transferID = 'TransferReq_' + str(receiverID) + '_' + get_random_string(length=10)
                getReceiverData = PayStackCustomerWalletDetails.objects.get(student_id = receiverID)
                getReceiverDataAcctNumber = getReceiverData.bank_account_number
                getReceiverCustomerID = getReceiverData.bank_customer_code
                getReceiverAccountName = getReceiverData.bank_account_name
                getReceiverBank = getReceiverData.bank_name

                # CHECK SENDER ACCOUNT BALANCE
                if PayStackCustomerWalletDetails.objects.get(student_id = GetSenderID):
                    senderPaystackWallet = PayStackCustomerWalletDetails.objects.get(student_id = GetSenderID)
                    senderPaystackWalletBalance = senderPaystackWallet.accountBalance     
                    senderPaystackCustomerCode = senderPaystackWallet.bank_customer_code
                
                    # CHECK IF BALANCE CAN SEND FUNDS 
                    if int(senderPaystackWalletBalance) < (int(serializer.data['transferAmount']) + 50.00):
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Sorry, you have an insufficient wallet balance. Kindly topup and try again"
                        })
                    else:
                        # SAVE DEBIT TRANSACTION IN WALLET
                        StudentWalletTransactionsSave = StudentWalletTransactions(user = request.user, SenderStudentID = GetSenderID, 
                            transactionID = transferID, transactionType = 'Debit', transactionCustomerPhone = fetchSenderPhoneNumber, 
                            transactionAmount = serializer.data['transferAmount'], transactionStatus = 'Pending', 
                            transactionCustomerCode = senderPaystackCustomerCode, receiverAccountNumber = getReceiverDataAcctNumber,
                            receiverCustomerID = getReceiverCustomerID, receiverAccountName =  getReceiverAccountName,
                            receiverAccountBank = getReceiverBank, receiverAccountStudentID = GetSenderID
                            )
                        # update sender account balance in DB 
                        findStudentSender = PayStackCustomerWalletDetails.objects.get(student_id=GetSenderID)
                        oldWalletBalance = int(PayStackCustomerWalletDetails.objects.get(student_id = GetSenderID).accountBalance)
                        newTransactionAmount = oldWalletBalance - int(serializer.data['transferAmount'] + 50)
                        newAccountBalance = {'accountBalance': newTransactionAmount}
                        serializer = UpdateWalletBalance(findStudentSender, data = newAccountBalance)
                        transferstatus = 'Pending'
                        newStudentAccountBalance = newTransactionAmount
                        amountToTransfer = transferAmount[0]
                        # 
                        if serializer.is_valid():
                            serializer.save()                    
                            # Send notification email
                            try:
                                TransferEmailNotification(request, senderEmail, senderFirstName, senderLastName, amountToTransfer, getReceiverAccountName, getReceiverBank, transferstatus, newStudentAccountBalance)
                            except:
                                print(f'email for transfer notification was not sent for user: {senderEmail}')
                            StudentWalletTransactionsSave.save()
                            print(f'{request.user.email} account balance updated')
                        else:
                            return Response({
                                        "status":status.HTTP_400_BAD_REQUEST,
                                        "message": 'An error occured',
                                        'error': serializer.error_messages
                                    })                        
                        
                        return Response({
                                        "status":status.HTTP_200_OK,
                                        "message": 'Nice! Your transfer request was sent successfully! Funds will arrive shortly'
                                    })                    
                else:
                    return Response({
                                "status":status.HTTP_400_BAD_REQUEST,
                                "message": 'You do not have a wallet yet',
                            })
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Sorry, the reciever does not own a wallet account on DHMS"
                }) 
        
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid data submitted",
                "error": serializer.error_messages
            }) 
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })   



@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def DashboardOverview(request):
    try:
        if StudentDHMSSignUp.objects.filter(student_email = request.user.email):
            FindStudentID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
            NumberOfDevices = StudentDeviceReg.objects.filter(student_admin_id = FindStudentID).count()
            NumberOfHealthyDevices = StudentDeviceReg.objects.filter(Q(student_admin_id = FindStudentID) & Q(student_device_health = 'Healthy')).count()
            NumberOfFaultyDevices = StudentDeviceReg.objects.filter(Q(student_admin_id = FindStudentID) & Q(student_device_health = 'Faulty')).count()
            NumberOfMaintenanceDevices = StudentMaintenanceRequest.objects.filter(student_admin_id = FindStudentID).count()
            NumberOfSubStudents = SubStudentRegistration.objects.filter(sub_student_admin_id = FindStudentID).count()
            
            overViewData = {
                'NumberOfDevices':NumberOfDevices, 'NumberOfHealthyDevices':NumberOfHealthyDevices, 'NumberOfFaultyDevices':NumberOfFaultyDevices,
                'NumberOfMaintenanceDevices':NumberOfMaintenanceDevices, 'NumberOfSubStudents':NumberOfSubStudents
            }
            return Response({
                "status": status.HTTP_200_OK,
                'overViewData':overViewData,
                "message": "Overview data found"
            }) 
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "User does not exit",
            })  
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })
    


@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CheckStudentPlan(request):
    try:
        StudentDHMSSignUp.objects.get(student_email = request.user.email)
        FindStudentID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
        if SubscribedUser.objects.filter(StudentID = FindStudentID):
            StudentPlan = SubscribedUser.objects.get(StudentID = FindStudentID).StudentPlan
            return Response({
                "status": status.HTTP_200_OK,
                'StudentPlan':StudentPlan,
                "message": "Student Plan Found"
            }) 
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "You Do Not Have An Existing Plan on The DHMS",
            })  
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })
    

# FETCH MAINTENANCE COUNTS
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FetchMaintenanceRequestCounts(request):
    # try:
        findCurrentUserID = StudentDHMSSignUp.objects.get(student_email = request.user.email).id
        StudentMaintenanceRequest.objects.filter(student_admin_id = findCurrentUserID)
        completedMaintenance = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(maintenance_status = 'Completed')).count()
        pendingMaintenance = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(maintenance_status = 'Pending')).count()
        ongoingMaintenance = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(maintenance_status = 'Ongoing')).count()
        declinedMaintenance = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(maintenance_status = 'Declined')).count()
        
        # get maintenance requests by month
        # allDevicesMonthPre = StudentMaintenanceRequest.objects.filter(student_admin_id = findCurrentUserID)
        # allDevicesMonth = allDevicesMonthPre.values_list('registeredMonth')
        JanMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'Jan'))
        JanMaintenanceReqsCount = JanMaintenanceReqs.count()
        FebMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'Feb'))
        FebMaintenanceReqsCount = FebMaintenanceReqs.count()
        MarMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'Mar'))
        MarMaintenanceReqsCount = MarMaintenanceReqs.count()
        AprMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'Apr'))
        AprMaintenanceReqsCount = AprMaintenanceReqs.count()
        MayMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'May'))
        MayMaintenanceReqsCount = MayMaintenanceReqs.count()
        JuneMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'Jun'))
        JuneMaintenanceReqsCount = JuneMaintenanceReqs.count()
        JulyMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'Jul'))
        JulyMaintenanceReqsCount = JulyMaintenanceReqs.count()
        AugMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'Aug'))
        AugMaintenanceReqsCount = AugMaintenanceReqs.count()
        SeptMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'Sep'))
        SeptMaintenanceReqsCount = SeptMaintenanceReqs.count()
        OctMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'Oct'))
        OctMaintenanceReqsCount = OctMaintenanceReqs.count()
        NovMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'Nov'))
        NovMaintenanceReqsCount = NovMaintenanceReqs.count()
        DecMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(student_admin_id = findCurrentUserID) & Q(registeredMonth = 'Dec'))
        DecMaintenanceReqsCount = DecMaintenanceReqs.count()
        # january = {
        #     'Jan':JanMaintenanceReqsCount,
        # }
        
#         maintenanceCountPerMonth": [
#               {"month":"Jan", "count": 0}
#          ]

        maintenanceReqsPerMonth = {
            'Jan':JanMaintenanceReqsCount,
            'Feb':FebMaintenanceReqsCount,
            'Mar':MarMaintenanceReqsCount,
            'Apr':AprMaintenanceReqsCount,
            'May':MayMaintenanceReqsCount,
            'June':JuneMaintenanceReqsCount,
            'July':JulyMaintenanceReqsCount,
            'Aug':AugMaintenanceReqsCount,
            'Sept':SeptMaintenanceReqsCount,
            'Oct':OctMaintenanceReqsCount,
            'Nov':NovMaintenanceReqsCount,
            'Dec':DecMaintenanceReqsCount,            
        }

        data = {
            'completedMaintenance': completedMaintenance, 
            'pendingMaintenance' : pendingMaintenance, 
            'ongoingMaintenance' : ongoingMaintenance, 
            'declinedMaintenance' : declinedMaintenance
        }
        
        return Response({
            "status": status.HTTP_200_OK,
            'maintenanceCountByStatus':data,
            'maintenanceCountPerMonth':maintenanceReqsPerMonth,
            "message": "Maintenance counts fetch successfull"
        }) 
    # except:
    #     return Response({
    #         "status": status.HTTP_400_BAD_REQUEST,
    #         "message": "An error occured. Kindly try again"
    #     })
    

@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FetchTechnicalPartners(request):
    try:
        FoundTechnicians = []
        if technicianModel.objects.filter():
            fetchAllTechnicians = technicianModel.objects.all()
            for fetchAllTechnician in fetchAllTechnicians:
                fetchAllTechnicianName = fetchAllTechnician.technicianName
                fetchAllTechnicianEmail = fetchAllTechnician.technicianEmail
                fetchAllTechnicianPhone = fetchAllTechnician.technicianPhoneNumber
                fetchAllTechnicianAvailability = fetchAllTechnician.technicianAvailability
                fetchAllTechnicianLocation = fetchAllTechnician.technicianLocation
                dateRegistered = fetchAllTechnician.created_at
                
                techniciansData = {
                    'technicianName': fetchAllTechnicianName, 'technicianEmail': fetchAllTechnicianEmail, 'technicianPhone': fetchAllTechnicianPhone,
                    'technicianAvailability': fetchAllTechnicianAvailability, 'technicianLocation': fetchAllTechnicianLocation, 
                    'dateRegistered': dateRegistered,
                }
                
                FoundTechnicians.append(techniciansData)
                
            return Response({
                "status": status.HTTP_200_OK,
                'techniciansData':FoundTechnicians,
                "message": "Technicians fetch successfull"
            }) 
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "No technician available",
            }) 
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured.",
        }) 
        

# Reassign device endpoint
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['PUT'], request_body = ReassignDeviceSerializer)
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ReassignDevice(request, id):
    try:
        serializer = ReassignDeviceSerializer(data = request.data)
        if serializer.is_valid():
            studentEmailAddress = serializer.data['substudentEmail']
            
            # find device 
            if StudentDeviceReg.objects.filter(id = id):
                getDevice = StudentDeviceReg.objects.get(id = id)
                getDeviceUserId = StudentDeviceReg.objects.get(id = id).student_user_id
                if getDeviceUserId is not None:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Device is already assigned to a student. Kindly unassign the device before reassiging it.",
                    })
                # find sub student
                if SubStudentRegistration.objects.filter(sub_student_email_address = studentEmailAddress):
                    findSubStudent = SubStudentRegistration.objects.get(sub_student_email_address = studentEmailAddress)
                    findSubStudentID = int(findSubStudent.id)
                    findSubStudentAdminID = int(findSubStudent.sub_student_admin_id)
                    findAdminID = int(StudentDHMSSignUp.objects.get(student_email = request.user.email).id)
                    # getDeviceUserId
                    if findSubStudentAdminID == findAdminID:
                        assignNewUser = {'student_user_id' :  findSubStudentID}  
                        print(findSubStudentID)
                        serialiseData = AllStudentDevicesSerializer(getDevice, data = assignNewUser)
                        if serialiseData.is_valid():
                            serialiseData.save()
                            return Response({
                                "status": status.HTTP_200_OK,
                                "message": "Device Reassigned successfull"
                            })
                        else:
                            return Response({
                                "status": status.HTTP_400_BAD_REQUEST,
                                "message": "An error occured.",
                                "error": serializer.error_messages
                            }) 
                    else:
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "The student is not under your jurisdiction.",
                        })
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Invalid email address provided",
                    })            
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "An error occured. The ID is invalid",
                }) 
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "An error occured.",
                "error": serializer.error_messages
            }) 
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured.",
        }) 




@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UnassignedDevices(request):
    try:
        allUnAssignedDevice = []
        finAdminID = int(StudentDHMSSignUp.objects.get(student_email = request.user.email).id)
        allDevices = StudentDeviceReg.objects.filter(Q(student_user_id = None) & Q(student_admin_id = finAdminID))
        for allDevice in allDevices:
            allDeviceID = allDevice.id
            allDeviceName = allDevice.device_name
            allDeviceSerialNumber = allDevice.device_serial_number
            allDeviceOS = allDevice.device_os
            allDeviceHealth = allDevice.student_device_health
            
            deviceData = {
                'DeviceID' : allDeviceID, 'DeviceName' : allDeviceName, 'DeviceSerialNumber': allDeviceSerialNumber,
                'DeviceOS': allDeviceOS, 'DeviceHealth': allDeviceHealth
            }
            
            allUnAssignedDevice.append(deviceData)
            
        return Response({
            "status": status.HTTP_200_OK,
            "unassignedDevice": allUnAssignedDevice,
            "message": "Device Reassigned successfull"
        }) 
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured.",
        }) 
    
    

@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def MaintenaceRequestIssueTypes(request):
    try:
        deviceStatuses = {
            'Screen Repairs':'Screen Repairs',
            'Battery Issues':'Battery Issues',
            'Keyboard Issues':'Keyboard Issues',
            'Motherboard Issues':'Motherboard Issues',
            'Others':'Others',
            }        
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Maintenance Request Issues Types',
            'data': deviceStatuses
        })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured'
        })





@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserProfileDetails(request):
    try:
        userProfileData = {
            'id': request.user.id,
            'firstname': request.user.first_name,
            'lastname': request.user.last_name,
            'email': request.user.email,
        }     
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Profile data fetch successfull',
            'data': userProfileData
        })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured'
        })


# Get user location
@swagger_auto_schema(tags=['StudentDHMSEndpoint'], methods=['POST'], request_body = GetLocationUsingLongLatSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def GetLocationUsingLongLat(request):
    try:        
        serializer = GetLocationUsingLongLatSerializer(data = request.data)
        if serializer.is_valid():
            lat = serializer.data['Latitude']
            long = serializer.data['Longitude']
            
            determinLocationWithOpencage = get_location_from_lat_long_opencage(lat, long)
            if determinLocationWithOpencage == 'No address found':
                print('location found')
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'No technician found in your location',
                })
            else:
                eachLocationWord = determinLocationWithOpencage.split()
                print(eachLocationWord)
                if ('Lagos' in eachLocationWord):
                    foundTechiciansResult = FindTechniciansInLocation('Lagos')                    
                    print('Lagos found')
                    return Response({
                        'status': status.HTTP_200_OK,
                        'message': 'We succcessfully found technicians in Lagos',
                        'location': foundTechiciansResult
                        # 'location': determinLocationWithOpencage
                    })
                elif('Imo' in eachLocationWord):
                    foundTechiciansResult = FindTechniciansInLocation('Imo')                    
                    print('Imo found')
                    return Response({
                        'status': status.HTTP_200_OK,
                        'message': 'We succcessfully found technicians in Imo',
                        'location': foundTechiciansResult
                        # 'location': determinLocationWithOpencage
                    })
                elif('Port Harcourt' in eachLocationWord):
                    foundTechiciansResult = FindTechniciansInLocation('Port Harcourt')                    
                    print('Lagos found')
                    return Response({
                        'status': status.HTTP_200_OK,
                        'message': 'We succcessfully found technicians in Port Harcourt',
                        'location': foundTechiciansResult
                        # 'location': determinLocationWithOpencage
                    })
                else:
                    return Response({
                        'status': status.HTTP_200_OK,
                        'message': 'No technician found in your location',
                    })
        
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'There was an error processing the longitude and latitude you provided.'
            })
    except:
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'An error occured, kindly try again'
        })

