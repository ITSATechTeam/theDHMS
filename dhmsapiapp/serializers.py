from typing import OrderedDict
from rest_framework import serializers
from dhmsadminboard.models import technicianModel
from studentdhms.models import *
from useronboard.models import SignupForm
from userarea.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupForm
        fields = ['companyname', 'email', 'phone', 'city', 'country', 'password', 'repassword']
        # fields = '__all__'


class OrgLoginSerializer(serializers.Serializer):
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


class StaffDataSetSerializer(serializers.ModelSerializer):
    class Meta:
        model= StaffDataSet
        fields = '__all__'
        # fields = ['StaffID', 'staff_firstname', 'staff_lastname', 'staff_phonenumber',
        #           'staff_email', 'staff_role', 'staff_location', 'CompanyUniqueCode']
        


# STUDENT DHMS TABLES STARTS HERE

class Student_Registration_Serializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDHMSSignUp
        fields = ['student_name', 'student_email', 'student_school', 'student_phone', 'student_password']



class StudentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class AccountValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model= StaffDataSet
        fields = '__all__'
    email = serializers.EmailField()
    password = serializers.CharField()



class UpdatePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.RegexField(
    regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
    write_only=True,
    error_messages={'invalid': ('Password must be at least 8 characters long with at least one capital letter and symbol')})
    confirm_password = serializers.CharField(write_only=True, required=True)



class TechnicalPartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = technicianModel
        fields = ['technicianEmail', 'technicianName', 'technicianPhoneNumber', 'technicianAvailability', 'technicianLocation', 'technicianUniqueID', 'created_at']


class SingleTechnicalPartnersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = technicianModel
        fields = ['technicianEmail']


class StudentDeviceRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDeviceReg
        fields = ['device_name', 'device_serial_number', 'device_os', 'student_user_email']


class SubStudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubStudentRegistration
        fields = ['sub_student_name', 'sub_student_email']