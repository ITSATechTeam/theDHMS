from django.db import models
from django.contrib.auth.models import User

TransferStatusOption = (
    ("Pending", "Pending"),
    ("Failed", "Failed"),
    ("Approved", "Approved"),
)
MaintainanceStatusOption = (
    ("Pending", "Pending"),
    ("Ongoing", "Ongoing"),
    ("Declined", "Declined"),
    ("Completed", "Completed"),
)

# Create your models here.

class StudentDHMSSignUp(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    student_firstname = models.CharField(max_length= 200, null=True, blank = True)
    student_lastname = models.CharField(max_length= 200, null=True, blank = True)
    student_email = models.EmailField(max_length= 200, null=True, blank = True)
    student_school = models.CharField(max_length= 200, null=True, blank = True)
    student_phone = models.CharField(max_length= 200, null=True, blank = True)
    student_password = models.CharField(max_length= 200, null=True, blank = True)
    accountActivationStatus = models.CharField(max_length= 200, null=True, blank = True, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.student_email} {self.student_firstname}'


class SubStudentRegistration(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    sub_student_firstname = models.CharField(max_length= 200, null=True, blank = True)
    sub_student_lastname = models.CharField(max_length= 200, null=True, blank = True)
    sub_student_email_address = models.EmailField(max_length= 200, null=True, blank = True)
    sub_student_phone_number = models.CharField(max_length= 200, null=True, blank = True)
    sub_student_school_name = models.CharField(max_length= 200, null=True, blank = True)
    sub_student_matric_number = models.CharField(max_length= 200, null=True, blank = True)
    # sub_student_admin_email = models.EmailField(max_length= 200, null=True, blank = True)
    sub_student_admin_id = models.CharField(max_length= 200, null=True, blank = True)
    sub_student_password = models.EmailField(max_length= 200, null=True, blank = True)
    accountActivationStatus = models.CharField(max_length= 200, null=True, blank = True, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.sub_student_firstname} {self.sub_student_email_address}'




class Password_Reset(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length= 200, null=True, blank = True)
    token = models.CharField(max_length= 200, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.email} {self.user}'



class StudentDeviceReg(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    student_admin_id = models.CharField(max_length= 200, null=True, blank = True)
    device_name = models.CharField(max_length= 200, null=True, blank = True)
    # device_name = models.CharField(max_length= 200, null=True, blank = True)
    device_serial_number = models.CharField(max_length= 200, null=True, blank = True)
    device_os = models.CharField(max_length= 200, null=True, blank = True)
    # student_user_email = models.EmailField(max_length= 200, null=True, blank = True)
    student_user_id = models.CharField(max_length= 200, null=True, blank = True)
    student_device_health = models.CharField(max_length= 200, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.student_user_id} is the user for: {self.device_name}'



class StudentMaintenanceRequest(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    student_requester_id = models.CharField(max_length= 200, null=True, blank = True)
    student_admin_id = models.CharField(max_length= 200, null=True, blank = True)
    device_id = models.CharField(max_length= 200, null=True, blank = True)
    device_name = models.CharField(max_length= 200, null=True, blank = True)
    maintenance_priority_level = models.CharField(max_length= 200, null=True, blank = True)
    maintenance_issue = models.CharField(max_length= 200, null=True, blank = True)
    maintenance_status = models.CharField(max_length= 300, choices = MaintainanceStatusOption, default = 'Pending')
    maintenance_description = models.CharField(max_length= 200, null=True, blank = True)
    registeredMonth = models.CharField(max_length = 1500, default=None, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.device_name} {self.maintenance_issue}'



class StudentTransactionPIN(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    student_id = models.CharField(max_length= 200, null=True, blank = True)
    student_transaction_pin = models.CharField(max_length= 200, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.student_id} {self.student_transaction_pin}'



class PayStackCustomerWalletDetails(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    accountBalance = models.IntegerField(default=0)
    bank_customer_code = models.CharField(max_length= 200, null=True, blank = True)
    student_id = models.CharField(max_length= 200, null=True, blank = True)
    # student_email_address = models.EmailField(max_length= 200, null=True, blank = True)
    bank_name = models.CharField(max_length= 200, null=True, blank = True)
    bank_name_slug = models.CharField(max_length= 200, null=True, blank = True)
    bank_account_name = models.CharField(max_length= 200, null=True, blank = True)
    bank_account_number = models.CharField(max_length= 200, null=True, blank = True)
    bank_account_currency = models.CharField(max_length= 200, null=True, blank = True)
    bank_account_creation_date = models.CharField(max_length= 200, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'Paystack customer code: {self.bank_customer_code}'
    


class StudentTransferRecipientCode(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    bank_customer_code = models.CharField(max_length= 200, null=True, blank = True)
    bank_account_number = models.CharField(max_length= 200, null=True, blank = True)
    student_id = models.CharField(max_length= 200, null=True, blank = True)
    recipient_code = models.CharField(max_length= 200, null=True, blank = True)
    recipient_id = models.CharField(max_length= 200, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.student_id} {self.recipient_code}'
    


class VerifyEmailAddress(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    studentID = models.CharField(max_length= 200, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.studentID} has been verified'


class VerifyPhoneNumber(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    studentID = models.CharField(max_length= 200, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.studentID} has been verified'



class StudentWalletTransactions(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank = True)
    StudentEmail = models.EmailField(max_length= 200, null=True, blank = True)
    SenderStudentID = models.CharField(max_length= 200, null=True, blank = True)
    transactionCustomerPhone = models.CharField(max_length= 200, null=True, blank = True)
    transactionCustomerCode = models.CharField(max_length= 200, null=True, blank = True)
    transactionID = models.CharField(max_length= 200, null=True, blank = True)
    transactionReference = models.CharField(max_length= 200, null=True, blank = True)
    transactionType = models.CharField(max_length= 200, null=True, blank = True)
    transactionMethod = models.CharField(max_length= 200, null=True, blank = True)
    transactionAmount = models.CharField(max_length= 200, null=True, blank = True)
    transactionStatus = models.CharField(max_length= 300,choices = TransferStatusOption, default = 'Pending', null=True, blank = True)
    # transactionStatus = models.CharField(max_length= 200, null=True, blank = True)
    transactionDateFromPaystack = models.CharField(max_length= 200, null=True, blank = True)
    transactionPOSData = models.CharField(max_length= 200, null=True, blank = True)
    paystackFeeForTransaction = models.CharField(max_length= 200, null=True, blank = True)
    transactionAuthCode = models.CharField(max_length= 200, null=True, blank = True)
    transactionNarration = models.CharField(max_length= 200, null=True, blank = True)
    transactionCardType = models.CharField(max_length= 200, null=True, blank = True)
    # if sending these fields will be filled
    receiverAccountNumber = models.CharField(max_length= 200, null=True, blank = True)
    receiverAccountStudentID = models.CharField(max_length= 200, null=True, blank = True)
    receiverCustomerID = models.CharField(max_length= 200, null=True, blank = True)
    receiverAccountName = models.CharField(max_length= 200, null=True, blank = True)
    receiverAccountBank = models.CharField(max_length= 200, null=True, blank = True)
    # if receiving these fields will be filled
    senderAccountNumber = models.CharField(max_length= 200, null=True, blank = True)
    senderAccountName = models.CharField(max_length= 200, null=True, blank = True)
    senderAccountBank = models.CharField(max_length= 200, null=True, blank = True)
    # 
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'Student ID: {self.user}'




class RegisterPaystackCustomers(models.Model):
    StudentID = models.CharField(max_length= 200, null=True, blank = True)
    customerCode = models.CharField(max_length= 200, null=True, blank = True)
    integration = models.CharField(max_length= 200, null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.customerCode}'



# class TransferRequests(models.Model):
#     user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank = True)    
#     senderStudentID = models.CharField(max_length= 200, null=True, blank = True)
#     transferAmount = models.CharField(max_length= 200, null=True, blank = True)
#     transferNarration = models.CharField(max_length= 200, null=True, blank = True)
#     #
#     receiverAccountNumber = models.CharField(max_length= 200, null=True, blank = True)
#     receiverBank = models.CharField(max_length= 200, null=True, blank = True)
#     receiverID = models.CharField(max_length= 200, null=True, blank = True)
#     receiverEmail = models.EmailField(max_length= 200, null=True, blank = True)
#     # 
#     transferStatus = models.CharField(max_length= 300,choices = TransferStatusOption, default = 'Pending', null=True, blank = True)
#     transferFeedback = models.CharField(max_length= 200, null=True, blank = True)
#     transferID = models.CharField(max_length= 300, null=True, blank = True)
#     # 
#     created_at = models.DateTimeField(auto_now_add=True)
#     edited_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-edited_at', '-created_at']
        
#     def __str__(self):
#         return f'Sender student ID: {self.senderStudentID}'



class SubscribedUser(models.Model):
    StudentID = models.CharField(max_length= 300, null=True, blank = True)
    StudentPlan = models.CharField(max_length= 300, null=True, blank = True)
    # 
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return f'{self.StudentID} with plan: {self.StudentPlan}'
    

