from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('navbar/', views.NavBar, name="NavBar"),
    path('pre_signup/', views.PreSignUpPage, name="PreSignUpPage"),
    path('signup/', views.SignUpPage, name="SignUpPage"),
    path('login/', views.Login, name="Login"),
    path('', views.Home, name="Home"),

    path("password_reset", views.password_reset_request, name="password_reset")

    
    # path('editcompanydetails/<str:id>/', views.EditUserSignupDetails, name="EditUserSignupDetails"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)