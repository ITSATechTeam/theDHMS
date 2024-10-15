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
from .utils import save_new_transactions
from .serializers import *
from userarea.models import *
from dhmsadminboard.models import *
from drf_yasg.utils import swagger_auto_schema
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
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
from requests import Response
from django.core.mail import send_mail, EmailMessage


def SendSubStudentEmailNotification(request, subStudentEmail, password, adminEmail, adminName):
    print('Send sub student email notification starts here.')
    print(subStudentEmail)
    recipient_list = [subStudentEmail]
    subStudentUser = SubStudentRegistration.objects.get(sub_student_email_address = subStudentEmail)
    subStudentFirstname = subStudentUser.sub_student_firstname
    subStudentLastname = subStudentUser.sub_student_lastname
    print(subStudentFirstname)
    print(subStudentLastname)
    context = {'firstName':subStudentFirstname, 'lastName':subStudentLastname, 'emailAddress':subStudentEmail, 'password':password,
                'adminEmail':adminEmail, 'adminName':adminName}
    html_message = render_to_string("mailouts/substudentonboardmail.html", context=context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject = "Your Have Been Added on The DHMS", 
        body = plain_message,
        from_email = 'dhmsinventoryapp@gmail.com',
        to= recipient_list
        )
    
    message.attach_alternative(html_message, "text/html")
    message.send()

    if message:
        print('Sent a notification email')
        return Response({
            "status":status.HTTP_200_OK,
            "message": "Email notification has been sent to sub student successfully.",
        })
    else:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": f'Problem sending notification email to {subStudentEmail}, check if you typed it correctly'
        })
    # except:
    #     return Response({
    #         "status": status.HTTP_400_BAD_REQUEST,
    #         "message": "An error occured."
    #     })

