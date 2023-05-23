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


class staffForm(ModelForm):
    class Meta:
        model = StaffDataSet
        fields = '__all__'


class DeviceRegisterForm(ModelForm):
    class Meta:
        model = DeviceRegisterUpload
        fields = '__all__'


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
