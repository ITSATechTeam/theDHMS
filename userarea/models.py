from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User


# Create your models here.



class StaffDataSet(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    deviceuserfirstname = models.CharField(max_length= 200, null=True, blank = True)
    deviceuserlastname = models.CharField(max_length= 200, null=True, blank = True)
    deviceuserphonenumber = models.CharField(max_length= 200, null=True, blank = True)
    deviceuseremail = models.CharField(max_length= 200, null=True, blank = True)
    staffDevice = models.CharField(max_length= 200, null=True, blank = True)
    staffrole = models.CharField(max_length= 200, null=True, blank = True)
    devicelocation = models.CharField(max_length= 200, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.deviceuserfirstname} {self.deviceuserphonenumber}'




class DeviceRegisterUpload(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    # staffUser = models.ForeignKey(StaffDataSet, null=True, on_delete=models.CASCADE)
    deviceip = models.CharField(max_length = 1500, null=True, blank = True)
    devicename= models.CharField(max_length = 1500, blank = True, null=True)
    devicemacaddress = models.CharField(max_length = 1500, null=True, blank = True)
    devicenetworkadaptercompany = models.CharField(max_length = 1500, null=True, blank = True)
    deviceuserfirstname = models.CharField(max_length= 200, null=True, blank = True)
    deviceuserlastname = models.CharField(max_length= 200, null=True, blank = True)
    devicestatus = models.CharField(max_length = 1500, null=True, blank = True)
    deviceworkgroup = models.CharField(max_length = 1500, null=True, blank = True)
    deviceusedepartment = models.CharField(max_length = 1500, null=True, blank = True)
    deviceportnumber = models.CharField(max_length = 1500, null=True, blank = True)
    devicemultiplepacket = models.CharField(max_length = 1500, null=True, blank = True)
    index= models.CharField(max_length = 1500, blank = True, null=True)
    devicetype= models.CharField(max_length = 1500, null=True, blank = True)
    devicelocation= models.CharField(max_length = 1500, null=True, blank = True)
    devicebrand= models.CharField(max_length = 1500, null=True, blank = True)
    deviceos = models.CharField(max_length = 1500, null=True, blank = True)
    devicecostofpurchase = models.CharField(max_length = 1500, null=True, blank = True)
    deviceuseremail = models.CharField(max_length= 200, null=True, blank = True)
    deviceuserphonenumber = models.CharField(max_length= 200, null=True, blank = True)
    deviceuserdateofresumption = models.CharField(max_length= 200, null=True, blank = True)
    deviceworkingcondition = models.CharField(max_length = 1500, null=True, blank = True)
    deviceyearofpurchase = models.CharField(max_length = 1500, null=True, blank = True)
    devicedepreciationrate = models.CharField(max_length = 1500, null=True, blank = True)
    deviceid = models.CharField(max_length = 1500, null=True, blank = True)
    savetimedata = models.CharField(max_length = 1500, null=True, blank = True)
    #
    # date = models.DateField(auto_now=False)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.deviceip} {self.devicename} {self.deviceuserfirstname}'
        # return f'{self.firstname} {self.lastname} {self.amountInvested} {self.plan} {self.created_at}'


class uploadedDeviceData(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length = 1500, null=True, blank = True)
    mainfile = models.FileField(upload_to='uploadedfiles/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    # def __str__(self):
    #     return self.user



class DeviceCountPerPage(models.Model):    
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    count = models.CharField(max_length= 3, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return self.count


class DeletedDevices(models.Model):    
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    deletedDeviceName = models.CharField(max_length= 3, null=True, blank = True)
    deletedDeviceMAC_ID = models.CharField(max_length= 3, null=True, blank = True)
    deletedDeviceID = models.CharField(max_length= 3, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return self.count



class MaintenanceRequest(models.Model):    
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    MaintainDeviceName = models.CharField(max_length= 300, null=True, blank = True)
    MaintainDeviceCategory = models.CharField(max_length= 300, null=True, blank = True)
    MaintainDeviceIP = models.CharField(max_length= 300, null=True, blank = True)
    MaintainType = models.CharField(max_length= 300, null=True, blank = True)
    MaintainStatus = models.CharField(max_length= 300, null=True, blank = True)
    MaintainDeviceLocation = models.CharField(max_length= 300, null=True, blank = True)
    MaintainDeviceUser = models.CharField(max_length= 300, null=True, blank = True)
    MaintainDeviceMAC_ID = models.CharField(max_length= 300, null=True, blank = True)
    MaintainDeviceID = models.CharField(max_length= 300, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return self.MaintainType












