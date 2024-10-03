from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class UserProfileImage(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    userReg = models.CharField(max_length=200, null=True, blank=True)
    profilepicture = models.ImageField(
        upload_to='profileimages/', blank=True, null=True)
        # upload_to='profileimages', blank=True, null=True, default="profileimages/default.png")
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return self.userReg


class SignupForm(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    companyname = models.CharField(max_length=200, null=True, blank=True)
    companyUniqueID = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)
    repassword = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return self.email


class LoginStatus(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length= 300, null=True, blank = True)
    status = models.CharField(max_length= 300, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return self.email
    

class AccountValidation(models.Model):
    userphonenumber = models.EmailField(max_length= 300, null=True, blank = True)
    useremail = models.EmailField(max_length= 300, null=True, blank = True)
    # activationStatus = models.CharField(max_length= 300, null=True, blank = True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=3)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return self.useremail
