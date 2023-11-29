from django.db import models
from django.contrib.auth.models import User

# Create your models here.



DEVICE_HEALTH_STATUS = (
    ("Working", "Working"),
    ("Faulty", "Faulty"),
    ("Critical", "Critical"),
)

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

        
class FamilyMemberReg(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    memberfullname = models.CharField(max_length = 1500, null=True, blank = True)
    memberemail = models.EmailField(max_length = 1500, null=True, blank = True)
    memberid = models.CharField(max_length = 1500, null=True, blank = True)
    familyid = models.CharField(max_length = 1500, null=True, blank = True)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.user} registered {self.memberfullname} with id {self.memberid}'




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
    deviceipaddress = models.CharField(max_length = 1500, null=True, blank = True)
    devicedepreciationrate = models.CharField(max_length = 1500, null=True, blank = True)
    deviceid = models.CharField(max_length = 1500, null=True, blank = True)
    deviceuser = models.CharField(max_length = 1500, null=True, blank = True)
    devicestatus = models.CharField(max_length= 300,choices = DEVICE_HEALTH_STATUS, default = 'Working', null=True, blank = True)    
    deviceImageOne = models.ImageField(upload_to='productImage/', null=True, blank=True)
    # deviceImageTwo = models.ImageField(upload_to='productImage/', null=True, blank=True)

    # SPECS FOR REGISTER MY DEVICE FEATURE STARTS HERE
    userbrowser = models.CharField(max_length = 1500, null=True, blank = True)
    userbrowserversion = models.CharField(max_length = 1500, null=True, blank = True)
    userOSVersion = models.CharField(max_length = 1500, null=True, blank = True)
    # SPECS FOR REGISTER MY DEVICE FEATURE ENDS HERE
    
    # DEVICE USER DETAILS STARTS HERE
    deviceUserID = models.CharField(max_length = 1500, default='None', null=True, blank = True)
    deviceuseremail = models.CharField(max_length= 200, null=True, blank = True)
    deviceuserfullname = models.CharField(max_length= 200, null=True, blank = True)
    # deviceUser = models.ForeignKey(FamilyMemberReg, null=True, on_delete=models.CASCADE)
    # DEVICE USER DETAILS ENDS HERE

    savetimedata = models.CharField(max_length = 1500, null=True, blank = True)
    registeredMonth = models.CharField(max_length = 1500, null=True, blank = True)
    weekNumberSaved = models.CharField(max_length = 1500, null=True, blank = True)
    FamilyUniqueCode = models.CharField(max_length = 130, null=True, blank = True)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.FamilyUniqueCode} {self.devicename} {self.deviceid} {self.devicetype}'



class FaultyDevicesTrend(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    deviceID = models.CharField(max_length = 1500, null=True, blank = True)
    month = models.CharField(max_length = 1500, null=True, blank = True)
    year = models.CharField(max_length = 1500, null=True, blank = True)
    FamilyUniqueCode = models.CharField(max_length = 130, null=True, blank = True)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.deviceID} got faulty in {self.month} and was reported by {self.user}'














