from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User


class UpdateFamilyMaintainanceReq(ModelForm):
    class Meta:
        model = FamilyMaintainanceReq
        fields = ['MaintainStatus']