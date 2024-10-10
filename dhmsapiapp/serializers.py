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
        fields = ['student_firstname', 'student_lastname', 'student_email', 'student_school', 'student_phone', 'student_password']


class Update_Student_Registration_Serializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDHMSSignUp
        fields = ['student_firstname', 'student_lastname', 'student_school', 'student_phone']
        # fields = ['student_firstname', 'student_lastname', 'student_email', 'student_school', 'student_phone']



class StudentLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AccountValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model= StaffDataSet
        fields = '__all__'
    email = serializers.EmailField()
    password = serializers.CharField()



class UpdatePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    

class UpdatePasswordSerializerWithPasswordFieldStudentModel(serializers.ModelSerializer):
    class Meta:
        model= StudentDHMSSignUp
        fields = ['student_password']



class UpdatePasswordSerializerWithPasswordField(serializers.Serializer):
    oldPassword = serializers.CharField(max_length= 50)
    newPassword = serializers.CharField(max_length= 50)
    # class Meta:
    #     model= User
        # fields = ['password']



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


class StudentDeviceRegSerializer(serializers.Serializer):
    student_user_email = serializers.EmailField()
    device_name = serializers.CharField()
    device_serial_number = serializers.CharField()
    device_os = serializers.CharField()
    student_device_health = serializers.CharField()
    



class DeviceSerializerForEdit(serializers.ModelSerializer):
    class Meta:
        model = StudentDeviceReg
        fields = ['device_name', 'device_serial_number', 'device_os', 'student_device_health']


class ReassignDeviceSerializer(serializers.Serializer):
    substudentEmail = serializers.EmailField()


class UpdateDeviceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDeviceReg
        fields = ['id', 'device_name', 'device_serial_number',]



class AllStudentDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDeviceReg
        fields = ['student_user_id']


class SubStudentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubStudentRegistration
        fields = ['sub_student_firstname', 'sub_student_lastname', 'sub_student_email_address', 'sub_student_phone_number', 'sub_student_school_name', 'sub_student_matric_number']


class FetchStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubStudentRegistration
        fields = ['id', 'sub_student_firstname', 'sub_student_lastname', 'sub_student_email_address', 'sub_student_phone_number', 'sub_student_school_name', 'sub_student_matric_number']


class FetchStudentSerializerForEdit(serializers.ModelSerializer):
    class Meta:
        model = SubStudentRegistration
        fields = ['sub_student_firstname', 'sub_student_lastname', 'sub_student_email_address', 'sub_student_phone_number', 'sub_student_school_name', 'sub_student_matric_number']



# DHMS SUPER ADMIN SERIALIZERS STARTS HERE
class ItsaSuperAdminLoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()



class UpdateDeviceAssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentDeviceReg
        fields = ['student_user_id']


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMaintenanceRequest
        fields = ['device_id', 'maintenance_priority_level', 
        'maintenance_issue', 'maintenance_description']



class FetchAllMaintenanceRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMaintenanceRequest
        fields = ['student_requester_id', 'device_name', 'maintenance_priority_level', 
        'maintenance_issue', 'maintenance_description', 'maintenance_status', 'created_at']




class GetEmailAddress(serializers.Serializer):
    email = serializers.EmailField()



class GetPhoneNumber(serializers.Serializer):
    phone = serializers.IntegerField()



class GetValidationCode(serializers.Serializer):
    code = serializers.CharField()


class StudentTransactionPINSerializer(serializers.Serializer):
    student_transaction_pin = serializers.CharField()



class UpdateStudentTransactionPINSerializer(serializers.Serializer):
    oldPin = serializers.CharField()
    newPin = serializers.CharField()
        


class FetchStudentTransactionPINSerializerForEdit(serializers.ModelSerializer):
    class Meta:
        model = StudentTransactionPIN
        fields = ['student_transaction_pin']
        
        
# class PayStackCustomerCreationSerializer(serializers.Serializer):
#     customer_firstname = serializers.CharField()
#     customer_lastname = serializers.CharField()
    


class ValidatePayStackCustomerSerializer(serializers.Serializer):
    # account_number = serializers.CharField()
    bvn = serializers.CharField()
    # bank_code = serializers.CharField()
    


class Device_Health_Status_Serializer(serializers.Serializer):
    Healthy = serializers.CharField()
    Faulty = serializers.CharField()
    Critical = serializers.CharField()


class SavePayStackCustomerWalletDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayStackCustomerWalletDetails
        fields = ['bank_name', 'bank_account_name', 'bank_account_number',
                  'bank_account_currency', 'bank_customer_code', 'bank_account_creation_date', 'student_id' ]    

    # def create(self, validated_data):
    #     # Get the authenticated user from the context
    #     user = self.context['request'].user
    #     profile = PayStackCustomerWalletDetails.objects.create(user=user, **validated_data)
    #     return profile

    

class FetchPayStackCustomerWalletDetails(serializers.ModelSerializer):
    class Meta:
        model = PayStackCustomerWalletDetails
        fields = ['bank_customer_code', 'student_id', 'bank_name', 'bank_name_slug', 'bank_account_name', 
                  'bank_account_number', 'bank_account_currency', 'bank_account_creation_date', 'accountBalance']


class VerifyUserAccountDetailsSerializer(serializers.Serializer):
    bank_code = serializers.CharField()
    account_number = serializers.CharField()
    

class SavePayStackRecipientIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentTransferRecipientCode
        fields = ['bank_customer_code', 'student_id', 'bank_account_number', 'recipient_code', 'recipient_id']
    

class InitializeFundTransferSerializer(serializers.Serializer):
    recipient_code = serializers.CharField()
    amount = serializers.IntegerField()
    reason = serializers.CharField()


class AccountBalanceSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    
    
class UpdateWalletBalance(serializers.ModelSerializer):
    class Meta:
        model = PayStackCustomerWalletDetails
        fields = ['accountBalance']
    

class SaveTransactionInDatabase(serializers.ModelSerializer):
    class Meta:
        model = StudentWalletTransactions
        fields = ['transactionType', 'StudentEmail', 'transactionAmount', 
                  'transactionStatus', 'partnerAccountNumber', 'partnerAccountName',
                  'partnerAccountBank','transactionDateFromPaystack', 'transactionPOSData',
                  'paystackFeeForTransaction', 'transactionAuthCode', 'transactionCardType',
                  'transactionNarration'
                  ]



class PlaceTransferRequestsSerializer(serializers.Serializer):
    transferAmount = serializers.IntegerField()
    receiverEmail = serializers.EmailField()
    transactionPIN = serializers.CharField()
        
        







