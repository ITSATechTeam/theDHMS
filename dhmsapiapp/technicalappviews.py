from dhmsapiapp.partnersserializers import *
from .serializers import *
import json
import os
from rest_framework import status
from django.conf import settings
from django.db.models.query_utils import Q
import hmac
import hashlib
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout, authenticate
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import extend_schema

        
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['post'], request_body=RegisterTechnicalPartnerSerializer)
@csrf_exempt
@api_view(['POST'])
def RegisterTechnicalPartner(request):
    try:
        if request.method == 'POST':
            serializer = RegisterTechnicalPartnerSerializer(data = request.data)
            if serializer.is_valid():
                technicianEmail = serializer.data['technicianEmail']
                technicianName = serializer.data['technicianName']
                technicianPhoneNumber = serializer.data['technicianPhoneNumber']
                technicianAvailability = serializer.data['technicianAvailability']
                technicianLocation = serializer.data['technicianLocation']
                password = serializer.data['password']
                
                if (technicianEmail is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing email address",
                        "error_message": serializer.error_messages
                    })
                if (technicianName is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing name",
                        "error_message": serializer.error_messages
                    })
                if (technicianPhoneNumber is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing phone number",
                        "error_message": serializer.error_messages
                    })
                if (technicianAvailability is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing availability. Kindly enter an availabily status",
                        "error_message": serializer.error_messages
                    })
                if (technicianLocation is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Missing location",
                        "error_message": serializer.error_messages
                    })
                    
                if technicianModel.objects.filter(technicianEmail = serializer.data['technicianEmail']).exists():
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Technical partner with this email already exists",
                    })             
                    
                    
                if technicianModel.objects.filter(technicianPhoneNumber = serializer.data['technicianPhoneNumber']).exists():
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Technical partner with this phone number already exists",
                    })
                    
                try:
                    form = technicianModel(technicianName=technicianName, technicianPhoneNumber = technicianPhoneNumber, technicianEmail = technicianEmail, 
                    password = password, technicianAvailability = technicianAvailability, technicianLocation = technicianLocation
                    )

                    userprofile = User.objects.create_user(username = technicianEmail, first_name = technicianName, 
                                    email = technicianEmail, last_name = technicianName, password = password)  
                    
                    # save user and technician profile info in DB
                    form.save()
                    userprofile.save()   
                                    
                    # Fetch data for creating tokens
                    getUserusername = technicianEmail
                    getUserPassword = password

                    tokenCreationDate = {
                        'username': getUserusername,
                        'password': getUserPassword
                    }
                    token_serializer = CustomTokenObtainPairSerializer(data=tokenCreationDate)
                    token_serializer.is_valid(raise_exception=True)
                    
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Technical partner profile created successfull.",
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
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "The data you provided are invalid, kindly check and try again.",
                    # "error_message": serializer.error_messages
                })
            
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error ocured, kindly try again.",
        })                                    


# Technician login endpoint
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['post'], request_body=LoginTechnicalPartnerSerializer)
@csrf_exempt
@api_view(['POST'])
def TechnicianPartnerLogin(request):
    # try:
    if request.method == 'POST':
        serializer = LoginTechnicalPartnerSerializer(data = request.data)
        if serializer.is_valid():
            technicianEmail = serializer.data['technicianEmail']
            password = serializer.data['password']
            if (technicianEmail is None):
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Missing email address",
                    "error_message": serializer.error_messages
                })
                
            if technicianModel.objects.filter(technicianEmail = technicianEmail).exists():                    
                # try:
                
                getTechnicianEmail = technicianEmail
                getTechnicianPassword = password
                tokenCreationData = {
                    'username': getTechnicianEmail,
                    'password': getTechnicianPassword
                }
                print('tokenCreationData')
                print(tokenCreationData)
                token_serializer = CustomTokenObtainPairSerializer(data=tokenCreationData)
                token_serializer.is_valid(raise_exception=True)
                
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Technical partner Login successfull.",
                    "Token": token_serializer.validated_data,
                    "data": serializer.data
                })
                
                # except:
                #     return Response({
                #         "status": status.HTTP_400_BAD_REQUEST,
                #         "message": "An error ocured, please try again"
                #     })  
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Error processing request. The email address is invalid",
                })
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Error processing data format. Kindly the information, and try again",
            })
            
    # except:
    #     return Response({
    #         "status": status.HTTP_400_BAD_REQUEST,
    #         "message": "An error ocured, kindly fill the form properly",
    #     })  

        
# Get maintenance requests tagged to logged in technician
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllMaintenanceRequest(request):
    AllMaintenanceRequests = []
    if StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email):
        AllRequests = StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email)
        for AllRequests in AllRequests:
            print(request.user.email)
            AllRequests_DeviceName = AllRequests.device_name
            AllRequests_RequesterUserEmail = AllRequests.user.email
            AllRequests_RequesterID = AllRequests.student_requester_id
            AllRequests_IssueTitle = AllRequests.maintenance_issue
            AllRequests_Decription = AllRequests.maintenance_description
            AllRequests_Status = AllRequests.maintenance_status
            AllRequests_DateRequested = AllRequests.created_at
            # check if requester is a student admin
            if StudentDHMSSignUp.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = StudentDHMSSignUp.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.student_email
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.student_school
            # check if requester is a sub student 
            elif SubStudentRegistration.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = SubStudentRegistration.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.sub_student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.sub_student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.sub_student_email_address
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.sub_student_school_name
            else:
                GetStudentAdminRequesterFirstName = None
                GetStudentAdminRequesterLastName = None
                GetStudentAdminRequesterEmail = None
                GetStudentAdminRequesterSchool = None
                
                
            # compile requests data
            AllRequests_Data = {
                "RequestDeviceName": AllRequests_DeviceName,
                "RequestTitle": AllRequests_IssueTitle,
                "RequestDecription": AllRequests_Decription,
                "RequestStatus": AllRequests_Status,
                "DateRequested": AllRequests_DateRequested,
                # Requester details
                "RequesterFirstName": GetStudentAdminRequesterFirstName,
                "RequesterLastName": GetStudentAdminRequesterLastName,
                "RequesterEmail": GetStudentAdminRequesterEmail,
                "RequesterSchool": GetStudentAdminRequesterSchool,
            }
        
            AllMaintenanceRequests.append(AllRequests_Data)
            
        return Response({
            "status": status.HTTP_200_OK,
            "AllMaintenanceRequests": AllMaintenanceRequests,
            "message": "Maintenance request fetch successfull",
        }) 
    else: 
        return Response({
            "status": status.HTTP_200_OK,
            "message": "You have no maintenance requests currently available.",
        }) 



# Get maintenance requests tagged to logged in technician
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetPendingMaintenanceRequest(request):
    AllMaintenanceRequests = []
    if StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email):
        AllRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Pending'))
        for AllRequests in AllRequests:
            AllRequests_DeviceName = AllRequests.device_name
            AllRequests_RequesterUserEmail = AllRequests.user.email
            AllRequests_RequesterID = AllRequests.student_requester_id
            AllRequests_IssueTitle = AllRequests.maintenance_issue
            AllRequests_Decription = AllRequests.maintenance_description
            AllRequests_Status = AllRequests.maintenance_status
            AllRequests_DateRequested = AllRequests.created_at
            # check if requester is a student admin
            if StudentDHMSSignUp.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = StudentDHMSSignUp.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.student_email
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.student_school
            # check if requester is a sub student 
            elif SubStudentRegistration.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = SubStudentRegistration.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.sub_student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.sub_student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.sub_student_email_address
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.sub_student_school_name
            else:
                GetStudentAdminRequesterFirstName = None
                GetStudentAdminRequesterLastName = None
                GetStudentAdminRequesterEmail = None
                GetStudentAdminRequesterSchool = None
                
                
            # compile requests data
            AllRequests_Data = {
                "RequestDeviceName": AllRequests_DeviceName,
                "RequestTitle": AllRequests_IssueTitle,
                "RequestDecription": AllRequests_Decription,
                "RequestStatus": AllRequests_Status,
                "DateRequested": AllRequests_DateRequested,
                # Requester details
                "RequesterFirstName": GetStudentAdminRequesterFirstName,
                "RequesterLastName": GetStudentAdminRequesterLastName,
                "RequesterEmail": GetStudentAdminRequesterEmail,
                "RequesterSchool": GetStudentAdminRequesterSchool,
            }
        
            AllMaintenanceRequests.append(AllRequests_Data)
            
        return Response({
            "status": status.HTTP_200_OK,
            "AllMaintenanceRequests": AllMaintenanceRequests,
            "message": "Maintenance request fetch successfull",
        }) 
    else: 
        return Response({
            "status": status.HTTP_200_OK,
            "message": "You have no maintenance requests currently available.",
        }) 


        
# Get maintenance requests tagged to logged in technician
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllMaintenanceCount(request):
    if StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email):
        AllRequests = StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email).count()
        PendingRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Pending')).count()
        OngoingRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Ongoing')).count()
        DeclinedRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Declined')).count()
        CompletedRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Completed')).count()
        
        maintenaceCount = {
            "AllRequests": AllRequests,
            "PendingRequests":PendingRequests,
            "OngoingRequests":OngoingRequests,
            "DeclinedRequests":DeclinedRequests,
            "CompletedRequests": CompletedRequests
        }
        return Response({
            "status": status.HTTP_200_OK,
            "maintenanceCount": maintenaceCount,
            "message": "Fetch maintenance request count was successful.",
        }) 
        
    else: 
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured.",
        }) 

# Get completed maintenance request percentage
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetCompletedMaintenancePercentage(request):
    if StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email):
        CompletedRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Completed')).count()
        AllRequests = StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email).count()
        CompletedMaintenacePercentage = CompletedRequests / AllRequests * 100
        return Response({
            "status": status.HTTP_200_OK,
            "CompletedMaintenacePercentage": f'{CompletedMaintenacePercentage}%',
            "message": "Fetch maintenance request count was successful.",
        }) 
    else:
        return Response({
        "status": status.HTTP_200_OK,
        "CompletedMaintenacePercentage": '0%',
        "message": "No maintenance request yet.",
        })


# Fetch maintenance requests for each technician 
@permission_classes([IsAuthenticated])
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
def FetchMaintenanceRequestPerMonth(request):
    try:
        completedMaintenance = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Completed')).count()
        pendingMaintenance = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Pending')).count()
        ongoingMaintenance = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Ongoing')).count()
        declinedMaintenance = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Declined')).count()
        
        # get maintenance requests by month
        JanMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'Jan'))
        JanMaintenanceReqsCount = JanMaintenanceReqs.count()
        FebMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'Feb'))
        FebMaintenanceReqsCount = FebMaintenanceReqs.count()
        MarMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'Mar'))
        MarMaintenanceReqsCount = MarMaintenanceReqs.count()
        AprMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'Apr'))
        AprMaintenanceReqsCount = AprMaintenanceReqs.count()
        MayMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'May'))
        MayMaintenanceReqsCount = MayMaintenanceReqs.count()
        JuneMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'Jun'))
        JuneMaintenanceReqsCount = JuneMaintenanceReqs.count()
        JulyMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'Jul'))
        JulyMaintenanceReqsCount = JulyMaintenanceReqs.count()
        AugMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'Aug'))
        AugMaintenanceReqsCount = AugMaintenanceReqs.count()
        SeptMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'Sep'))
        SeptMaintenanceReqsCount = SeptMaintenanceReqs.count()
        OctMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'Oct'))
        OctMaintenanceReqsCount = OctMaintenanceReqs.count()
        NovMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'Nov'))
        NovMaintenanceReqsCount = NovMaintenanceReqs.count()
        DecMaintenanceReqs = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(registeredMonth = 'Dec'))
        DecMaintenanceReqsCount = DecMaintenanceReqs.count()


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
            # 'maintenanceCountByStatus':data,
            'maintenanceCountPerMonth':maintenanceReqsPerMonth,
            "message": "Maintenance counts fetch successfull"
        }) 
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })
    

# Get maintenace request task percentage by maintenance issue type
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetMaintenanceTypePercentage(request):
    try:
        if StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email):
            AllRequests = StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email).count()
            AllScreenRepairRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_issue = 'Screen Repairs')).count()
            AllScreenRepairRequestsPercentage = AllScreenRepairRequests / AllRequests * 100
            AllBattertyRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_issue = 'Battery Issues')).count()
            AllBattertyRequestsPercentage = AllBattertyRequests / AllRequests * 100
            AllKeyboardRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_issue = 'Keyboard Issues')).count()
            AllKeyboardRequestsPercentage = AllKeyboardRequests / AllRequests * 100
            AllMotherBoardRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_issue = 'Motherboard Issues')).count()
            AllMotherBoardRequestsPercentage = AllMotherBoardRequests / AllRequests * 100
            AllOtherRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_issue = 'Others')).count()
            AllOtherRequestsPercentage = AllOtherRequests / AllRequests * 100
            
            maintenanceTyePercentages = {
                "ScreenRepairPercentage": f'{AllScreenRepairRequestsPercentage}%',
                "BatteryRepairPercentage": f'{AllBattertyRequestsPercentage}%',
                "KeyboardRepairPercentage": f'{AllKeyboardRequestsPercentage}%',
                "MotherBoardRepairPercentage": f'{AllMotherBoardRequestsPercentage}%',
                "OtherRepairPercentage": f'{AllOtherRequestsPercentage}%',
            }
            return Response({
                "status": status.HTTP_200_OK,
                "maintenanceTyePercentages": maintenanceTyePercentages,
                "message": "Fetch maintenance request rates was successful.",
            }) 
        else:
            return Response({
            "status": status.HTTP_200_OK,
            "CompletedMaintenacePercentage": '0%',
            "message": "No maintenance request yet.",
            })
    
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })

      
# Get last five maintenance requests tagged to logged in technician
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetLatestFiveMaintenanceRequest(request):
    AllMaintenanceRequests = []
    if StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email):
        AllRequests = StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email)
        LatestFiveMaintenanceRequests = AllRequests[:6]
        for AllRequests in LatestFiveMaintenanceRequests:
            print(request.user.email)
            AllRequests_DeviceName = AllRequests.device_name
            AllRequests_RequesterUserEmail = AllRequests.user.email
            AllRequests_RequesterID = AllRequests.student_requester_id
            AllRequests_IssueTitle = AllRequests.maintenance_issue
            AllRequests_Decription = AllRequests.maintenance_description
            AllRequests_Status = AllRequests.maintenance_status
            AllRequests_DateRequested = AllRequests.created_at
            # check if requester is a student admin
            if StudentDHMSSignUp.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = StudentDHMSSignUp.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.student_email
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.student_school
            # check if requester is a sub student 
            elif SubStudentRegistration.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = SubStudentRegistration.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.sub_student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.sub_student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.sub_student_email_address
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.sub_student_school_name
            else:
                GetStudentAdminRequesterFirstName = None
                GetStudentAdminRequesterLastName = None
                GetStudentAdminRequesterEmail = None
                GetStudentAdminRequesterSchool = None
                
                
            # compile requests data
            AllRequests_Data = {
                "RequestDeviceName": AllRequests_DeviceName,
                "RequestTitle": AllRequests_IssueTitle,
                "RequestDecription": AllRequests_Decription,
                "RequestStatus": AllRequests_Status,
                "DateRequested": AllRequests_DateRequested,
                # Requester details
                "RequesterFirstName": GetStudentAdminRequesterFirstName,
                "RequesterLastName": GetStudentAdminRequesterLastName,
                "RequesterEmail": GetStudentAdminRequesterEmail,
                "RequesterSchool": GetStudentAdminRequesterSchool,
            }
        
            AllMaintenanceRequests.append(AllRequests_Data)
            
        return Response({
            "status": status.HTTP_200_OK,
            "AllMaintenanceRequests": AllMaintenanceRequests,
            "message": "Maintenance request fetch successfull",
        }) 
    else: 
        return Response({
            "status": status.HTTP_200_OK,
            "message": "You have no maintenance requests currently available.",
        }) 


# MAINTENANCE PAGE ENDPOINTS STARTS HERE
# Get maintenance requests tagged to logged in technician
        
# Get maintenance requests tagged to logged in technician
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllMaintenanceRequest(request):
    AllMaintenanceRequests = []
    if StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email):
        AllRequests = StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email)
        for AllRequests in AllRequests:
            print(request.user.email)
            AllRequests_ID = AllRequests.id
            AllRequests_DeviceName = AllRequests.device_name
            AllRequests_RequesterUserEmail = AllRequests.user.email
            AllRequests_RequesterID = AllRequests.student_requester_id
            AllRequests_IssueTitle = AllRequests.maintenance_issue
            AllRequests_Decription = AllRequests.maintenance_description
            AllRequests_Status = AllRequests.maintenance_status
            AllRequests_DateRequested = AllRequests.created_at
            # check if requester is a student admin
            if StudentDHMSSignUp.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = StudentDHMSSignUp.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.student_email
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.student_school
            # check if requester is a sub student 
            elif SubStudentRegistration.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = SubStudentRegistration.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.sub_student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.sub_student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.sub_student_email_address
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.sub_student_school_name
            else:
                GetStudentAdminRequesterFirstName = None
                GetStudentAdminRequesterLastName = None
                GetStudentAdminRequesterEmail = None
                GetStudentAdminRequesterSchool = None
                
                
            # compile requests data
            AllRequests_Data = {
                "RequestID": AllRequests_ID,
                "RequestDeviceName": AllRequests_DeviceName,
                "RequestTitle": AllRequests_IssueTitle,
                "RequestDecription": AllRequests_Decription,
                "RequestStatus": AllRequests_Status,
                "DateRequested": AllRequests_DateRequested,
                # Requester details
                "RequesterFirstName": GetStudentAdminRequesterFirstName,
                "RequesterLastName": GetStudentAdminRequesterLastName,
                "RequesterEmail": GetStudentAdminRequesterEmail,
                "RequesterSchool": GetStudentAdminRequesterSchool,
            }
        
            AllMaintenanceRequests.append(AllRequests_Data)
            
        return Response({
            "status": status.HTTP_200_OK,
            "AllMaintenanceRequests": AllMaintenanceRequests,
            "message": "Maintenance request fetch successfull",
        }) 
    else: 
        return Response({
            "status": status.HTTP_200_OK,
            "message": "You have no maintenance requests currently available.",
        }) 


# get completed maintenance requests
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetCompletedMaintenanceRequest(request):
    CompletedMaintenanceRequests = []
    if StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email):
        AllRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Completed'))
        for AllRequests in AllRequests:
            AllRequests_ID = AllRequests.id
            AllRequests_DeviceName = AllRequests.device_name
            AllRequests_RequesterUserEmail = AllRequests.user.email
            AllRequests_RequesterID = AllRequests.student_requester_id
            AllRequests_IssueTitle = AllRequests.maintenance_issue
            AllRequests_Decription = AllRequests.maintenance_description
            AllRequests_Status = AllRequests.maintenance_status
            AllRequests_DateRequested = AllRequests.created_at
            # check if requester is a student admin
            if StudentDHMSSignUp.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = StudentDHMSSignUp.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.student_email
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.student_school
            # check if requester is a sub student 
            elif SubStudentRegistration.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = SubStudentRegistration.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.sub_student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.sub_student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.sub_student_email_address
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.sub_student_school_name
            else:
                GetStudentAdminRequesterFirstName = None
                GetStudentAdminRequesterLastName = None
                GetStudentAdminRequesterEmail = None
                GetStudentAdminRequesterSchool = None
                
                
            # compile requests data
            AllRequests_Data = {
                "RequestID": AllRequests_ID,
                "RequestDeviceName": AllRequests_DeviceName,
                "RequestTitle": AllRequests_IssueTitle,
                "RequestDecription": AllRequests_Decription,
                "RequestStatus": AllRequests_Status,
                "DateRequested": AllRequests_DateRequested,
                # Requester details
                "RequesterFirstName": GetStudentAdminRequesterFirstName,
                "RequesterLastName": GetStudentAdminRequesterLastName,
                "RequesterEmail": GetStudentAdminRequesterEmail,
                "RequesterSchool": GetStudentAdminRequesterSchool,
            }
        
            CompletedMaintenanceRequests.append(AllRequests_Data)
            
        return Response({
            "status": status.HTTP_200_OK,
            "CompletedMaintenanceRequests": CompletedMaintenanceRequests,
            "message": "Completed maintenance request fetch successfull",
        }) 
    else:
        return Response({
            "status": status.HTTP_200_OK,
            "message": "You have no completed maintenance requests currently.",
        }) 


# get Ongoing maintenance requests
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetOngoingMaintenanceRequest(request):
    OngoingMaintenanceRequests = []
    if StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email):
        AllRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Ongoing'))
        for AllRequests in AllRequests:
            AllRequests_ID = AllRequests.id
            AllRequests_DeviceName = AllRequests.device_name
            AllRequests_RequesterUserEmail = AllRequests.user.email
            AllRequests_RequesterID = AllRequests.student_requester_id
            AllRequests_IssueTitle = AllRequests.maintenance_issue
            AllRequests_Decription = AllRequests.maintenance_description
            AllRequests_Status = AllRequests.maintenance_status
            AllRequests_DateRequested = AllRequests.created_at
            # check if requester is a student admin
            if StudentDHMSSignUp.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = StudentDHMSSignUp.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.student_email
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.student_school
            # check if requester is a sub student 
            elif SubStudentRegistration.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = SubStudentRegistration.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.sub_student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.sub_student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.sub_student_email_address
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.sub_student_school_name
            else:
                GetStudentAdminRequesterFirstName = None
                GetStudentAdminRequesterLastName = None
                GetStudentAdminRequesterEmail = None
                GetStudentAdminRequesterSchool = None
                
                
            # compile requests data
            AllRequests_Data = {
                "RequestID": AllRequests_ID,
                "RequestDeviceName": AllRequests_DeviceName,
                "RequestTitle": AllRequests_IssueTitle,
                "RequestDecription": AllRequests_Decription,
                "RequestStatus": AllRequests_Status,
                "DateRequested": AllRequests_DateRequested,
                # Requester details
                "RequesterFirstName": GetStudentAdminRequesterFirstName,
                "RequesterLastName": GetStudentAdminRequesterLastName,
                "RequesterEmail": GetStudentAdminRequesterEmail,
                "RequesterSchool": GetStudentAdminRequesterSchool,
            }
        
            OngoingMaintenanceRequests.append(AllRequests_Data)
            
        return Response({
            "status": status.HTTP_200_OK,
            "OngoingMaintenanceRequests": OngoingMaintenanceRequests,
            "message": " Ongoing maintenance request fetch successfull",
        }) 
    else:
        return Response({
            "status": status.HTTP_200_OK,
            "message": "You have no Ongoing maintenance requests currently.",
        }) 


# get Declined maintenance requests
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['get'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetDeclinedMaintenanceRequest(request):
    DeclinedMaintenanceRequests = []
    if StudentMaintenanceRequest.objects.filter(techicianInCharge = request.user.email):
        AllRequests = StudentMaintenanceRequest.objects.filter(Q(techicianInCharge = request.user.email) & Q(maintenance_status = 'Declined'))
        for AllRequests in AllRequests:
            AllRequests_ID = AllRequests.id
            AllRequests_DeviceName = AllRequests.device_name
            AllRequests_RequesterUserEmail = AllRequests.user.email
            AllRequests_RequesterID = AllRequests.student_requester_id
            AllRequests_IssueTitle = AllRequests.maintenance_issue
            AllRequests_Decription = AllRequests.maintenance_description
            AllRequests_Status = AllRequests.maintenance_status
            AllRequests_DateRequested = AllRequests.created_at
            # check if requester is a student admin
            if StudentDHMSSignUp.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = StudentDHMSSignUp.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.student_email
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.student_school
            # check if requester is a sub student 
            elif SubStudentRegistration.objects.filter(id = AllRequests_RequesterID):
                GetStudentAdminRequester = SubStudentRegistration.objects.get(id = AllRequests_RequesterID)
                GetStudentAdminRequesterFirstName = GetStudentAdminRequester.sub_student_firstname
                GetStudentAdminRequesterLastName = GetStudentAdminRequester.sub_student_lastname
                GetStudentAdminRequesterEmail = GetStudentAdminRequester.sub_student_email_address
                GetStudentAdminRequesterSchool = GetStudentAdminRequester.sub_student_school_name
            else:
                GetStudentAdminRequesterFirstName = None
                GetStudentAdminRequesterLastName = None
                GetStudentAdminRequesterEmail = None
                GetStudentAdminRequesterSchool = None
                
                
            # compile requests data
            AllRequests_Data = {
                "RequestID": AllRequests_ID,
                "RequestDeviceName": AllRequests_DeviceName,
                "RequestTitle": AllRequests_IssueTitle,
                "RequestDecription": AllRequests_Decription,
                "RequestStatus": AllRequests_Status,
                "DateRequested": AllRequests_DateRequested,
                # Requester details
                "RequesterFirstName": GetStudentAdminRequesterFirstName,
                "RequesterLastName": GetStudentAdminRequesterLastName,
                "RequesterEmail": GetStudentAdminRequesterEmail,
                "RequesterSchool": GetStudentAdminRequesterSchool,
            }
        
            DeclinedMaintenanceRequests.append(AllRequests_Data)
            
        return Response({
            "status": status.HTTP_200_OK,
            "DeclinedMaintenanceRequests": DeclinedMaintenanceRequests,
            "message": " Declined maintenance request fetch successfull",
        }) 
    else:
        return Response({
            "status": status.HTTP_200_OK,
            "message": "You have no Declined maintenance requests currently.",
        }) 

        
@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['post'], request_body=SearchSerializer)
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SearchDevices(request):
    SearchResult = []
    try:
        if request.method == 'POST':
            serializer = SearchSerializer(data = request.data)
            if serializer.is_valid():
                searchKeyword = serializer.data['searchKeyword']
                
                if (searchKeyword is None):
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "No search term entered, kindly enter a device name to search.",
                    })
                #
                deviceSearch = StudentMaintenanceRequest.objects.filter(
                    Q(Q(device_name__icontains = searchKeyword) | 
                        Q(maintenance_issue__icontains = searchKeyword) |
                        Q(maintenance_description__icontains = searchKeyword) |
                        Q(device_id__icontains = searchKeyword) |
                        Q(maintenance_priority_level__icontains = searchKeyword) |
                        Q(registeredMonth__icontains = searchKeyword)) 
                    & Q(techicianInCharge = request.user.email)
                )            
                #  
                for deviceSearch in deviceSearch:
                    DeviceID = deviceSearch.id
                    DeviceName = deviceSearch.device_name
                    RequesterUserEmail = deviceSearch.user.email
                    RequesterID = deviceSearch.student_requester_id
                    IssueTitle = deviceSearch.maintenance_issue
                    Decription = deviceSearch.maintenance_description
                    Status = deviceSearch.maintenance_status
                    DateRequested = deviceSearch.created_at
                    # check if requester is a student admin
                    if StudentDHMSSignUp.objects.filter(id = RequesterID):
                        GetStudentAdminRequester = StudentDHMSSignUp.objects.get(id = RequesterID)
                        GetStudentAdminRequesterFirstName = GetStudentAdminRequester.student_firstname
                        GetStudentAdminRequesterLastName = GetStudentAdminRequester.student_lastname
                        GetStudentAdminRequesterEmail = GetStudentAdminRequester.student_email
                        GetStudentAdminRequesterSchool = GetStudentAdminRequester.student_school
                    # check if requester is a sub student
                    elif SubStudentRegistration.objects.filter(id = RequesterID):
                        GetStudentAdminRequester = SubStudentRegistration.objects.get(id = RequesterID)
                        GetStudentAdminRequesterFirstName = GetStudentAdminRequester.sub_student_firstname
                        GetStudentAdminRequesterLastName = GetStudentAdminRequester.sub_student_lastname
                        GetStudentAdminRequesterEmail = GetStudentAdminRequester.sub_student_email_address
                        GetStudentAdminRequesterSchool = GetStudentAdminRequester.sub_student_school_name
                    else:
                        GetStudentAdminRequesterFirstName = None
                        GetStudentAdminRequesterLastName = None
                        GetStudentAdminRequesterEmail = None
                        GetStudentAdminRequesterSchool = None                    
                        
                    # compile requests data
                    AllRequests_Data = {
                        "DeviceID": DeviceID,
                        "DeviceName": DeviceName,
                        "Title": IssueTitle,
                        "Decription": Decription,
                        "Status": Status,
                        "DateCreated": DateRequested,
                        # Requester details
                        "RequesterFirstName": GetStudentAdminRequesterFirstName,
                        "RequesterLastName": GetStudentAdminRequesterLastName,
                        "RequesterEmail": GetStudentAdminRequesterEmail,
                        "RequesterSchool": GetStudentAdminRequesterSchool,
                    }
                
                    SearchResult.append(AllRequests_Data)
                    
                if len(SearchResult) < 1:
                    return Response({
                    "status": status.HTTP_200_OK,
                    "message": "No search result found.",
                    })

                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Search result fetched successfully.",
                    "SearchResult": SearchResult
                })
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Error processing request",
                    "error_message": serializer.error_messages
                })
            
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error ocured, kindly fill the form properly",
        })                                    
 

@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['GET'])
@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetSingleMaintenance(request, id):
    if StudentMaintenanceRequest.objects.filter(id = id):
        getMaintenance = StudentMaintenanceRequest.objects.get(id = id)
        if getMaintenance.techicianInCharge == request.user.email:
            maintenanceIssue = getMaintenance.maintenance_issue            
            maintenanceDescription = getMaintenance.maintenance_description            
            maintenanceStatus = getMaintenance.maintenance_status            
            requesterID = getMaintenance.student_requester_id            
            requesterStudentStatus = getMaintenance.student_requester_status            
            requestPriority = getMaintenance.maintenance_priority_level            
            dateCreated = getMaintenance.created_at
            
            if requesterStudentStatus == 'StudentAdmin':
                GetStudentAdminRequester = StudentDHMSSignUp.objects.get(id = requesterID)
                reqeusterFirstName = GetStudentAdminRequester.student_firstname
                reqeusterLastName = GetStudentAdminRequester.student_lastname
                reqeusterEmail = GetStudentAdminRequester.student_email
                reqeusterPhone = GetStudentAdminRequester.student_phone
                reqeusterSchool = GetStudentAdminRequester.student_school
                
            elif requesterStudentStatus == 'SubStudent':
                GetStudentAdminRequester = SubStudentRegistration.objects.get(id = requesterID)
                reqeusterFirstName = GetStudentAdminRequester.sub_student_firstname
                reqeusterLastName = GetStudentAdminRequester.sub_student_lastname
                reqeusterEmail = GetStudentAdminRequester.sub_student_email_address
                reqeusterPhone = GetStudentAdminRequester.sub_student_phone_number
                reqeusterSchool = GetStudentAdminRequester.sub_student_school_name
                
            else:
                reqeusterFirstName = None
                reqeusterLastName = None
                reqeusterEmail = None
                reqeusterPhone = None
                reqeusterSchool = None                
            
            requesterData = {
                'firstName': reqeusterFirstName,
                'lastName': reqeusterLastName,
                'email': reqeusterEmail,
                'phone': reqeusterPhone,
                'School': reqeusterSchool,
            }
            
            maintenanceDetails = {
                'maintenanceID': id,
                'maintenanceIssue': maintenanceIssue,
                'maintenanceDescription': maintenanceDescription,
                'maintenanceStatus': maintenanceStatus,
                'requesterData': requesterData,
                'requestPriority': requestPriority,
                'dateCreated': dateCreated,
            }            
            
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Maintenance request found.",
                "data": maintenanceDetails
            })
            
        else:
            return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Maintenance request with this ID was not found under requests assigned to you.",
            })
    else:
        return Response({
        "status": status.HTTP_400_BAD_REQUEST,
        "message": "Maintenance request with the ID was not found.",
        })



@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['PUT'], request_body= GetChangeMaintenanceStatusSerializerData)
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def ChangeMaintenanceStatus(request):
    if technicianModel.objects.filter(technicianEmail = request.user.email):
        getCurrentTechnician = technicianModel.objects.get(technicianEmail = request.user.email)
        getCurrentTechnicianEmail = getCurrentTechnician.technicianEmail
        serializer = GetChangeMaintenanceStatusSerializerData(data = request.data)
        if serializer.is_valid():
            MaintenanceID = serializer.data['MaintenanceID']
            newStatus = serializer.data['newMaintenanceStatus']
            if newStatus not in ['Pending', 'Ongoing', 'Completed', 'Declined']:
                print('newStatus')     
                print(newStatus)     
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Maintenance status update failed. Maintenance status has to be either Pending, Ongoing, Completed or Declined.",
                })
                
            if StudentMaintenanceRequest.objects.filter(id = MaintenanceID):
                getMaintenance = StudentMaintenanceRequest.objects.get(id = MaintenanceID)
                getTechnicianEmail = getMaintenance.techicianInCharge
                
                # authorize technician to make this change
                if getTechnicianEmail != getCurrentTechnicianEmail:     
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "You are not authorized to update the maintenance status of this request.",
                    })
                    
                # update maintenance status from here
                newStatusToUpdate = {'maintenance_status': newStatus}
                serializer = ChangeMaintenanceStatusSerializer(getMaintenance, data = newStatusToUpdate)
                if serializer.is_valid():
                    serializer.save()
                    # maintenanceStatus = serializer.validated_data.get('maintenanceStatus')
                    # getMaintenance.maintenance_status = maintenanceStatus
                    # getMaintenance.save()
                    
                    return Response({
                        "status": status.HTTP_200_OK,
                        "message": "Maintenance status updated successfully.",
                        # "data": maintenanceDetails
                    })
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Maintenance request with the ID was not found.",
                })
                
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Maintenance request found.",
                # "data": maintenanceDetails
            })
        else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "The information you provided in invalid. Please check and try again.",
                })
    else:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "You do not have access to edit this information.",
        })

# The device with the provided ID is not assigned to you.

