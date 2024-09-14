from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(SubStudentRegistration)
admin.site.register(Password_Reset)
admin.site.register(StudentDeviceReg)
admin.site.register(StudentDHMSSignUp)
admin.site.register(StudentMaintenanceRequest)
admin.site.register(StudentTransactionPIN)
admin.site.register(PayStackCustomerWalletDetails)
admin.site.register(StudentTransferRecipientCode)
admin.site.register(VerifyEmailAddress)
admin.site.register(StudentWalletTransactions)
admin.site.register(RegisterPaystackCustomers)
admin.site.register(TransferRequests)

