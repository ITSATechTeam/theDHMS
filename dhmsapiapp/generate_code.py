
from useronboard.models import *
from dhmsadminboard.models import *
# from .views import GetEmailValidationCode
import datetime
import re
from time import strftime
from django.utils import timezone
import random
from django.shortcuts import redirect
# from datetime import datetime, timedelta
from django.utils import timezone

def generate_validation_code(request, email_address):
    print('timezone.now()')
    print(timezone.now())
    if(AccountValidation.objects.filter(useremail=email_address)):
        LatestAccountValidationEntry = AccountValidation.objects.filter(useremail=email_address).first()
        print('LatestAccountValidationEntry')
        print(LatestAccountValidationEntry)
        userMaxOTPTry = LatestAccountValidationEntry.max_otp_try
        userMaxOut = LatestAccountValidationEntry.otp_max_out
        userOTPExpiry = LatestAccountValidationEntry.otp_expiry
        
        if int(userMaxOTPTry) <= 3 and userMaxOut is None:
            otp = random.randint(1000, 9999)
            userMaxOTPTryNew = int(userMaxOTPTry) -1
            otp_user_waittime = timezone.now() + datetime.timedelta(hours=1)
            otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
            AccountValidationSave = AccountValidation.objects.create(useremail = email_address,otp = otp,  otp_expiry = otp_expiry, otp_max_out = otp_user_waittime,  max_otp_try = userMaxOTPTryNew)
            AccountValidationSave.save()
            return otp
        
        if int(userMaxOTPTry) == 1:
            otp = random.randint(1000, 9999)
            otp_user_waittime = timezone.now() + datetime.timedelta(hours=1)
            print('otp_user_waittime')
            print(otp_user_waittime)
            userMaxOTPTryNew = int(userMaxOTPTry) -1
            # GetEmailValidationCode(request, otp, email_address)
            otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
            AccountValidation.objects.create(useremail = email_address,otp = otp,  otp_expiry = otp_expiry, otp_max_out = otp_user_waittime, max_otp_try = userMaxOTPTryNew)
            return otp

        elif int(userMaxOTPTry) <= 0 and timezone.now() < userMaxOut:            
        # FORMAT REMAINING TIME SECTION ENDS HERE
            remainingTime = userMaxOut - timezone.now() 
            duration = str(remainingTime)
            dot_index = duration.find('.')
            if dot_index != -1:
                part_before_dot = duration[:dot_index]
            else:
                part_before_dot = duration
            print(part_before_dot)

            colon_index = part_before_dot.find(':')
            if colon_index != -1:
                part_after_colon = part_before_dot[colon_index + 1:]
            else:
                part_after_colon = part_before_dot 
                
            dot_index2 = part_after_colon.find(':')
            if dot_index2 != -1:
                FinalDuration = part_after_colon[:dot_index2]
            else:
                FinalDuration = part_after_colon
        # FORMAT REMAINING TIME SECTION ENDS HERE
            return 'CODE SENT'
        

        elif int(userMaxOTPTry) >= 0 and timezone.now() > userOTPExpiry:
            otp = random.randint(1000, 9999)
            userMaxOTPTryNew = 3
            otp_user_waittime = None
            # otp_user_waittime = timezone.now() + datetime.timedelta(hours=1)
            # GetEmailValidationCode(request, otp, email_address)
            otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
            AccountValidation.objects.create(useremail = email_address, otp = otp, otp_expiry = otp_expiry, otp_max_out = otp_user_waittime,  max_otp_try = userMaxOTPTryNew)
            return otp
        
        elif int(userMaxOTPTry) <= 0 and timezone.now() < userOTPExpiry:                    
        # FORMAT REMAINING TIME SECTION ENDS HERE        
            remainingTime = userMaxOut - timezone.now() 
            duration = str(remainingTime)
            dot_index = duration.find('.')
            if dot_index != -1:
                part_before_dot = duration[:dot_index] 
            else:
                part_before_dot = duration 
            print(part_before_dot)

            colon_index = part_before_dot.find(':')
            if colon_index != -1:
                part_after_colon = part_before_dot[colon_index + 1:]
            else:
                part_after_colon = part_before_dot 
                
            dot_index2 = part_after_colon.find(':')
            if dot_index2 != -1:
                FinalDuration = part_after_colon[:dot_index2]
            else:
                FinalDuration = part_after_colon                           
            return 'CODE SENT'
        
        elif int(userMaxOTPTry) < 0 and timezone.now() > userOTPExpiry:
            # messages.error(request, f'OTP Expired, kindly login again to recieve a new OTP')
            return 'CODE EXPIRED'

        else:
            # messages.error(request, f'An error occured')
            return 'CODE SENT' 
    else:
        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        otp_user_waittime = None
        # otp_user_waittime = timezone.now() + datetime.timedelta(hours=1)
        max_otp_try = 3
        AccountValidationSave = AccountValidation.objects.create(useremail = email_address, otp = otp, otp_expiry = otp_expiry, otp_max_out = otp_user_waittime, max_otp_try = max_otp_try)
        AccountValidationSave.save()
        return otp
    



def Verify_otp(emailAddress, code):
    # try:
    GetOTP = AccountValidation.objects.filter(useremail = emailAddress).first()
    if timezone.now() > GetOTP.otp_expiry:
        return 'CODE EXPIRED'

    if code == GetOTP.otp:
        AccountValidation.objects.filter(useremail = emailAddress).delete()
        return 'CODE VALIDATED'
    else:
        return 'CODE INVALID'

