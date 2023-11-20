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


class FamilyDeviceReg(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    devicetype = models.CharField(max_length = 1500, default='None')
    devicebrand = models.CharField(max_length= 200, null=True, blank = True)
    deviceOS = models.CharField(max_length= 200, null=True, blank = True)
    devicemodel = models.CharField(max_length= 200, null=True, blank = True)
    deviceyearofpurchase = models.CharField(max_length= 200, null=True, blank = True)
    devicelocation = models.CharField(max_length= 200, null=True, blank = True)
    devicename = models.CharField(max_length= 200, null=True, blank = True)
    devicemacaddress = models.CharField(max_length= 200, null=True, blank = True)    
    # deviceworkingcondition = models.CharField(max_length= 300,choices = DEVICE_WORKING_CONDITION, default = 'Good', null=True, blank = True)
    deviceipaddress = models.CharField(max_length = 1500, null=True, blank = True)
    devicedepreciationrate = models.CharField(max_length = 1500, null=True, blank = True)
    deviceid = models.CharField(max_length = 1500, null=True, blank = True)
    deviceuser = models.CharField(max_length = 1500, null=True, blank = True)

    savetimedata = models.CharField(max_length = 1500, null=True, blank = True)
    registeredMonth = models.CharField(max_length = 1500, null=True, blank = True)
    weekNumberSaved = models.CharField(max_length = 1500, null=True, blank = True)
    FamilyUniqueCode = models.CharField(max_length = 130, null=True, blank = True)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.FamilyUniqueCode} {self.devicename} {self.deviceid} {self.deviceuser}'
