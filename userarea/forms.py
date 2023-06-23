from django.forms import ModelForm
from django import forms
from django_countries.widgets import CountrySelectWidget
from .models import *
from useronboard.models import SignupForm, UserProfileImage
from django.contrib.auth.models import User


class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UpdateUserFromUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['last_name']


class staffForm(ModelForm):
    class Meta:
        model = StaffDataSet
        fields = ['staff_firstname', 'staff_lastname', 'staff_phonenumber',
        'staff_email', 'staff_role', 'staff_location'
        ]


class DeviceRegisterForm(ModelForm):
    class Meta:
        model = DeviceRegisterUpload
        # fields = '__all__'
        fields = ['deviceip', 'devicename', 'devicemacaddress', 'devicestatus', 'devicetype', 'deviceyearofpurchase',
        'devicebrand', 'deviceos', 'devicecostofpurchase', 'devicelocation', 'staffUserID', 'deviceusedepartment'
        ]


class UpdateDeviceUser(ModelForm):
    class Meta:
        model = DeviceRegisterUpload
        fields = ['staffUserID']


class ProfileImageUpload(ModelForm):
    class Meta:
        model = UserProfileImage
        fields = ['profilepicture']


class UserRegistrationForm(forms.ModelForm):
    # profileImg = forms.ImageField()
    companyname = forms.CharField(max_length=32)
    email = forms.CharField(max_length=32)
    class Meta:
        model = SignupForm
        fields = ['user', 'companyname', 'email', 'phone', 'city', 'country', 'address']



# STATUS_CHOICES= [
#     ('Ongoing', 'Ongoing'),
#     ('Completed', 'Completed'),
#     ('Canceled', 'Cancelede'),
#     ]


class EditMaintenanceRequest(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['MaintainStatus', 'MaintainRequestDescription']
