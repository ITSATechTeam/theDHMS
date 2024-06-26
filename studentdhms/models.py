from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StudentDHMSSignUp(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    student_username = models.CharField(max_length= 200, null=False, blank = False)
    student_name = models.CharField(max_length= 200, null=False, blank = False)
    student_email = models.EmailField(max_length= 200, null=False, blank = False)
    student_school = models.CharField(max_length= 200, null=False, blank = False)
    # student_phone = models.IntegerField(blank = False)
    student_password = models.CharField(max_length= 200, null=False, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.student_email} {self.student_username}'


