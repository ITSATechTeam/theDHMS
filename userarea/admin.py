from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(SignupUser)
# admin.site.register(RegisterStaff)
admin.site.register(DeviceRegisterUpload)
admin.site.register(uploadedDeviceData)
admin.site.register(StaffDataSet)
admin.site.register(DeviceCountPerPage)
admin.site.register(MaintenanceRequest)