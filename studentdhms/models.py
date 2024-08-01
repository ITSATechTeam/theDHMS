from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentDHMSSignUp(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    student_name = models.CharField(max_length= 200, null=False, blank = False)
    student_email = models.EmailField(max_length= 200, null=False, blank = False)
    student_school = models.CharField(max_length= 200, null=False, blank = False)
    student_phone = models.IntegerField(blank = False)
    student_password = models.CharField(max_length= 200, null=False, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.student_email} {self.student_name}'


class SubStudentRegistration(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    sub_student_name = models.CharField(max_length= 200, null=False, blank = False)
    sub_student_email = models.EmailField(max_length= 200, null=False, blank = False)
    sub_student_admin_email = models.EmailField(max_length= 200, null=False, blank = False)
    sub_student_password = models.EmailField(max_length= 200, null=False, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.sub_student_name} {self.sub_student_email}'




class Password_Reset(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length= 200, null=False, blank = False)
    token = models.CharField(max_length= 200, null=False, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.student_email} {self.student_username}'



class StudentDeviceReg(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    student_admin_email = models.EmailField(max_length= 200, null=False, blank = False)
    device_name = models.CharField(max_length= 200, null=False, blank = False)
    device_serial_number = models.CharField(max_length= 200, null=False, blank = False)
    device_os = models.CharField(max_length= 200, null=False, blank = False)
    student_user_email = models.EmailField(max_length= 200, null=False, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.student_admin_email} {self.device_name}'


