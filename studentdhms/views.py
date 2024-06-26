from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def DefaultView(request):
    return HttpResponse(request, 'working')