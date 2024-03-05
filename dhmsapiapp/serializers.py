from rest_framework import serializers
from useronboard.models import SignupForm
from userarea.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupForm
        fields = '__all__'



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



class LogoutSerializer(serializers.Serializer):
    id = serializers.IntegerField
    

class GetOrgDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupForm
        fields = ['id']
    # id = serializers.IntegerField
    
    
class AllDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceRegisterUpload
        fields = '__all__'
