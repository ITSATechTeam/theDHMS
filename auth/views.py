from django.shortcuts import render

# Create your views here.
def AuthRedirect(request):
    return render(request, 'staffapp/staffdashboard.html')