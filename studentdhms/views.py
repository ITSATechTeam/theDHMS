from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import random
from .models import *
from useronboard.models import SignupForm
from userarea.models import *
# Create your views here.




def DefaultView(request):
    return HttpResponse(request, 'working')


def StudentLogin(request):
    if request.method == 'POST':
        student_email = request.POST['email']
        student_password = request.POST['password']
        CheckUserUsername = User.objects.get(email = student_email).username
        try:
            user = User.objects.get(username=CheckUserUsername)
        except:
            messages.error(request, 'Login Failed: Please Try Again .')
            return redirect('StudentLogin')
        
        user = authenticate(request, username=user, password=student_password)

        if user is not None:
            login(request, user)
            return redirect('StudentDashboard')

        else:
            # print(error)
            messages.error(request, 'Login Failed: Please Try Again or Contact Your IT Admin.')
            return redirect('StudentLogin')
    return render(request, 'studentdhms/studentlogin.html')



# STUDENT LOGIN ENDPOINT
@login_required(login_url='StudentLogin')
def StudentDashboard(request):
    return render(request, 'studentdhms/studentdashboard.html')

