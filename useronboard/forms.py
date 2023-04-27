from .models import *
from django.forms import ModelForm


class UserRegistrationForm(ModelForm):
    class Meta:
        model = SignupForm
        fields = '__all__'

