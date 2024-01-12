from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import *
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from datetime import date
from django.db.models import Q
import json

# Create your views here.

def SuperAdminAccess(request):
    return render(request, 'dhmsadminboard/superadminlogin.html')