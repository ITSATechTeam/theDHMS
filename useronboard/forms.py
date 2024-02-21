from .models import *
from django.forms import ModelForm
from allauth.socialaccount.forms import SignupForm as SignupForm2


class UserRegistrationForm(ModelForm):
    class Meta:
        model = SignupForm
        fields = '__all__'




class CustomSocialSignupForm(SignupForm2):
    # Add or override fields as needed
    companyname = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return self.companyname
    
