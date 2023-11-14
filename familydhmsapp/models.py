from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Familyregister(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length= 200, null=True, blank = True)
    fullname = models.CharField(max_length= 200, null=True, blank = True)
    password = models.CharField(max_length= 200, null=True, blank = True)
    familyUniqueID = models.CharField(max_length= 200, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.fullname} {self.familyUniqueID}'

