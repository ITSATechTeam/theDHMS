from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Familyregister)
admin.site.register(FamilyDeviceReg)
admin.site.register(FamilyMemberReg)
admin.site.register(FaultyDevicesTrend)
admin.site.register(FamilyMaintainanceReq)
admin.site.register(FamilySubAdmin)

