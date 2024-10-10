from enum import Enum
from typing import OrderedDict
from rest_framework import serializers
from dhmsadminboard.models import technicianModel
from studentdhms.models import *
from useronboard.models import SignupForm
from userarea.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class TechnicalPartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = technicianModel
        fields = ['technicianEmail', 'technicianName', 'technicianPhoneNumber', 'technicianAvailability', 'technicianLocation', 'technicianUniqueID', 'created_at']


class RegisterTechnicalPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = technicianModel
        fields = ['technicianEmail', 'technicianName', 'technicianPhoneNumber', 'technicianAvailability', 'technicianLocation', 'password']



class LoginTechnicalPartnerSerializer(serializers.Serializer):
    technicianEmail = serializers.EmailField()
    password = serializers.CharField()


class SingleTechnicalPartnersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = technicianModel
        fields = ['technicianEmail']

