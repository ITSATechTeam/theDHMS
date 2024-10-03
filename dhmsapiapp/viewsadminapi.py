import json
import os
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
import hmac
import hashlib
from venv import logger
from django.dispatch import receiver
from grpc import Status
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from dhmsapiapp.generate_code import Verify_otp, generate_validation_code
from dhmsapiapp.generaterandomnum import generate_unique_number
from django.http import JsonResponse

from .utils import save_new_transactions  # Import the function
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
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.forms import PasswordResetForm

from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from enum import Enum
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



@swagger_auto_schema(methods=['get'])
@csrf_exempt
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def GetAllDHMSMaintenanceReqs(request):
    FoundMainRequests = []
    try:
        currentMaintenanceRequestMain = MaintenanceRequest.objects.all()
        AllStaffData = StaffDataSet.objects.all()
        if currentMaintenanceRequestMain.count() > 1:
            for currentMaintenanceRequest in currentMaintenanceRequestMain:
                if StaffDataSet.objects.filter(StaffID = currentMaintenanceRequest.MaintainDeviceUserID):
                    AttachedStaffUser = StaffDataSet.objects.get(StaffID = currentMaintenanceRequest.MaintainDeviceUserID)
                    MaintainDeviceUserFirstName = AttachedStaffUser.staff_firstname
                    MaintainDeviceUserLastName = AttachedStaffUser.staff_lastname
                else:
                    MaintainDeviceUserFirstName = None
                    MaintainDeviceUserLastName = None
                MaintainDeviceName = currentMaintenanceRequest.MaintainDeviceName
                MaintainDeviceUserID = currentMaintenanceRequest.MaintainDeviceUserID
                MaintainDeviceUserFirstName = MaintainDeviceUserFirstName
                MaintainDeviceUserLastName = MaintainDeviceUserLastName
                # MaintainDeviceUserFirstName = AttachedStaffUser.values_list('staff_firstname', flat=True)
                # MaintainDeviceUserLastName = AttachedStaffUser.values_list('staff_lastname', flat=True)
                MaintainDeviceLocation = currentMaintenanceRequest.MaintainDeviceLocation
                MaintainDeviceID = currentMaintenanceRequest.MaintainDeviceID
                MaintainDeviceUserDepartment = currentMaintenanceRequest.MaintainDeviceUserDepartment
                MaintainStatus = currentMaintenanceRequest.MaintainStatus
                created_at = currentMaintenanceRequest.created_at
                
                SpecificDeviceUserData = {
                    "MaintainDeviceUserFirstName":MaintainDeviceUserFirstName, "MaintainDeviceUserLastName":MaintainDeviceUserLastName,
                }
                FoundMaintenanceRequests = {
                    "MaintainDeviceName":MaintainDeviceName, "DeviceUser":SpecificDeviceUserData, "MaintainStatus":MaintainStatus,
                    "MaintainDeviceLocation":MaintainDeviceLocation, "MaintainDeviceID":MaintainDeviceID, "MaintainDeviceUserDepartment":MaintainDeviceUserDepartment,
                    "date_registered":created_at
                }
                FoundMainRequests.append(FoundMaintenanceRequests)        
                
            return Response({
                "status":status.HTTP_200_OK,
                "message": "Maintenance Requests found",
                "data": FoundMainRequests
            })
        else:
            currentMaintenanceRequest = MaintenanceRequest.objects.all()
            MaintainDeviceName = currentMaintenanceRequest.MaintainDeviceName
            MaintainDeviceUserID = currentMaintenanceRequest.MaintainDeviceUserID
            MaintainDeviceLocation = currentMaintenanceRequest.MaintainDeviceLocation
            MaintainDeviceID = currentMaintenanceRequest.MaintainDeviceID
            MaintainDeviceUserDepartment = currentMaintenanceRequest.MaintainDeviceUserDepartment
            MaintainStatus = currentMaintenanceRequest.MaintainStatus
            created_at = currentMaintenanceRequest.created_at
                
            FoundMaintenanceRequests = {
                    "MaintainDeviceName":MaintainDeviceName, "MaintainDeviceUserID":MaintainDeviceUserID, "MaintainStatus":MaintainStatus,
                    "MaintainDeviceLocation":MaintainDeviceLocation, "MaintainDeviceID":MaintainDeviceID, "MaintainDeviceUserDepartment":MaintainDeviceUserDepartment,
                    "date_registered":created_at
                }
            
            FoundMainRequests.append(FoundMaintenanceRequests)            
            
            return Response({
                "status":status.HTTP_200_OK,
                "message": "Maintenance Requests found",
                "data": FoundMainRequests
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })


@swagger_auto_schema(methods=['get'])
@csrf_exempt
@api_view(['GET'])
def FetchAllOrganization(request):
    FoundOrganizations = []
    try:
        AllOrganizations = SignupForm.objects.all()
        # AllStaffData = StaffDataSet.objects.all()
        if AllOrganizations.count() > 1:
            for currentCompany in AllOrganizations:
                # staff count
                if StaffDataSet.objects.filter(CompanyUniqueCode = currentCompany.companyUniqueID):
                    StaffDataSetCount = StaffDataSet.objects.filter(CompanyUniqueCode = currentCompany.companyUniqueID).count()
                    # staffName = StaffDataSetCount.values_list('staff_firstname', flat=True) + StaffDataSetCount.values_list('staff_lastname', flat=True)
                else:
                    StaffDataSetCount = 0
                    # Device count
                if DeviceRegisterUpload.objects.filter(CompanyUniqueCode = currentCompany.companyUniqueID):
                    DeviceCount = StaffDataSet.objects.filter(CompanyUniqueCode = currentCompany.companyUniqueID).count()
                else:
                    DeviceCount = 0
                organizationID = currentCompany.id
                companyname = currentCompany.companyname
                companyUniqueID = currentCompany.companyUniqueID
                companyEmail = currentCompany.email
                companyPhone = currentCompany.phone
                companyLocation = currentCompany.city
                companyAddress = currentCompany.address
                created_at = currentCompany.created_at                    
                
                FoundCompanyDetails = {'organizationID':organizationID,
                    "companyname":companyname, "companyUniqueID":companyUniqueID, 'DeviceCount':DeviceCount,
                    "companyEmail":companyEmail, "companyPhone":companyPhone, 'StaffDataSetCount' : StaffDataSetCount,
                    "companyLocation":companyLocation, "companyAddress":companyAddress,
                    "date_registered":created_at
                }
                
                FoundOrganizations.append(FoundCompanyDetails)        
                
            return Response({
                "status":status.HTTP_200_OK,
                "message": "Organizations found",
                "data": FoundOrganizations
            })
        else:
            AllOrganizations = SignupForm.objects.all().first()
            for currentCompany in AllOrganizations:
                if StaffDataSet.objects.filter(CompanyUniqueCode = currentCompany.companyUniqueID):
                    StaffDataSetCount = StaffDataSet.objects.filter(CompanyUniqueCode = currentCompany.companyUniqueID).count()
                    # staffName = StaffDataSetCount.values_list('staff_firstname', flat=True) + StaffDataSetCount.values_list('staff_lastname', flat=True)
                else:
                    StaffDataSetCount = 0
                    # Device count
                if DeviceRegisterUpload.objects.filter(CompanyUniqueCode = currentCompany.companyUniqueID):
                    DeviceCount = StaffDataSet.objects.filter(CompanyUniqueCode = currentCompany.companyUniqueID).count()
                else:
                    DeviceCount = 0
            organizationID = currentCompany.id
            companyname = AllOrganizations.companyname
            companyUniqueID = AllOrganizations.companyUniqueID
            companyEmail = AllOrganizations.email
            companyPhone = AllOrganizations.phone
            companyLocation = AllOrganizations.city
            companyAddress = AllOrganizations.address
            created_at = AllOrganizations.created_at
                
            FoundCompanyDetails = {'organizationID':organizationID,
                    "companyname":companyname, "companyUniqueID":companyUniqueID, 'DeviceCount':DeviceCount,
                    "companyEmail":companyEmail, "companyPhone":companyPhone, 'StaffDataSetCount': StaffDataSetCount,
                    "companyLocation":companyLocation, "companyAddress":companyAddress,
                    "date_registered":created_at
                }
            
            FoundOrganizations.append(FoundCompanyDetails)            
            
            return Response({
                "status":status.HTTP_200_OK,
                "message": "Organizations found",
                "data": FoundOrganizations
            })
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })



@swagger_auto_schema(methods=['get'])
@csrf_exempt
@api_view(['GET'])
def FetchOrganizationDetails(request):
    id = request.GET.get('id')
    try:
        FindOrganization = SignupForm.objects.get(id = id)
        # fetch organization
        if(FindOrganization):
            organizationName = FindOrganization.companyname
            organizationEmail = FindOrganization.email
            organizationPhone = FindOrganization.phone
            organizationCity = FindOrganization.city
            organizationCountry = FindOrganization.country
            organizationAddress = FindOrganization.address
            organizationUniqueID = FindOrganization.companyUniqueID
            
            companyData = {
                'organizationName':organizationName, 'organizationEmail':organizationEmail,
                'organizationPhone':organizationPhone, 'organizationCity':organizationCity,
                'organizationCountry':organizationCountry, 'organizationAddress':organizationAddress,
                'organizationUniqueID':organizationUniqueID
            }

            return Response({
                "status":status.HTTP_200_OK,
                "message": "Organizations found",
                "data": companyData
            })

        else:
            return Response({
                "status":status.HTTP_400_BAD_REQUEST,
                "message": "An error occured",
            })

    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })

        




        
