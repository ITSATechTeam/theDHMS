
from dhmsapiapp.partnersserializers import *
from .serializers import *
import json
import os
from rest_framework import status
from django.conf import settings
import hmac
import hashlib
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
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
                    
                # testpartner@gmail.com
                try:
                    form = technicianModel(technicianName=technicianName, technicianPhoneNumber = technicianPhoneNumber, technicianEmail = technicianEmail, 
                    password = password, technicianAvailability = technicianAvailability, technicianLocation = technicianLocation
                    )

                    userprofile = User.objects.create_user(username = technicianEmail, first_name = technicianName, email = technicianEmail, 
                                    last_name = technicianName, password = password)  
                    
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
                    "message": "Error processing request",
                    "error_message": serializer.error_messages
                })
            
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error ocured, kindly fill the form properly",
            "error": serializer.error_messages
        })                                    


@swagger_auto_schema(tags=['TechnicalPartnersEndpoint'], methods=['post'], request_body=LoginTechnicalPartnerSerializer)
@csrf_exempt
@api_view(['POST'])
def TechnicianPartnerLogin(request):
    try:
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
                    try:
                        partnerUserAuth = authenticate(request, username=technicianEmail, password=password)  
                        if partnerUserAuth is not None:
                            login(request, partnerUserAuth)             
                            # create tokens

                            tokenCreationDate = {
                                'username': technicianEmail,
                                'password': password
                            }
                            token_serializer = CustomTokenObtainPairSerializer(data=tokenCreationDate)
                            token_serializer.is_valid(raise_exception=True)
                            
                            return Response({
                                "status": status.HTTP_200_OK,
                                "message": "Technical partner Login successfull.",
                                "Token": token_serializer.validated_data,
                                "data": serializer.data
                            })
                        else:
                            return Response({
                                "status": status.HTTP_400_BAD_REQUEST,
                                "message": "Authentication failed, please try again"
                            })  
                    
                    except:
                        return Response({
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "An error ocured, please try again"
                        })  
                else:
                    return Response({
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Error processing request. Kindly check your information and try again",
                    })
            else:
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Error processing data format. Kindly the information, and try again",
                })
                
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error ocured, kindly fill the form properly",
            "error": serializer.error_messages
        })  
        