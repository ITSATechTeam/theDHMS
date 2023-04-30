from django.urls import path
from . import views


urlpatterns = [
    path('navbar/', views.NavBar, name="NavBar"),
    path('', views.PreSignUpPage, name="PreSignUpPage"),
    path('signup/', views.SignUpPage, name="SignUpPage"),
    path('login/', views.Login, name="Login"),

    path("password_reset", views.password_reset_request, name="password_reset")

    
    # path('editcompanydetails/<str:id>/', views.EditUserSignupDetails, name="EditUserSignupDetails"),
]