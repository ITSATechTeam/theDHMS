from django.urls import path
from . import views


urlpatterns = [
    path('navbar/', views.NavBar, name="NavBar"),
    path('presignup/', views.PreSignUpPage, name="PreSignUpPage"),
    path('', views.SignUpPage, name="SignUpPage"),
    path('login/', views.Login, name="Login"),
    # path('editcompanydetails/<str:id>/', views.EditUserSignupDetails, name="EditUserSignupDetails"),
]