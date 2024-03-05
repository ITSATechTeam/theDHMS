# # from site import USER_BASE
# from django.urls import reverse
# from django.contrib import messages
# from .models import *
# from useronboard.models import LoginStatus
# from .forms import *
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.utils.crypto import get_random_string
# from django.contrib.auth import login, logout, authenticate

# def login_cancelled(request):
#     AllMaintenanceRequests = MaintenanceRequest.objects.filter(CompanyUniqueCode = request.user.last_name)
#     allSignUps = SignupForm.objects.filter(user = request.user)
#     context = {'allSignUps': allSignUps, 'AllMaintenanceRequests':AllMaintenanceRequests}
#     return render(request, 'general.html', context)