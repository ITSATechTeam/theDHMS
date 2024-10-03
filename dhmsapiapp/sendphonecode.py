from twilio.rest import Client
import requests
from rest_framework.response import Response
from rest_framework import status

account_SID = "ACfeef096fdd3bae26dccba586b62a8209"
account_token = "b59dfe4937f113b1911334e7fad65a6a"
twilio_phn = "+15075563221"
# twilio_phn = "DHMS"
# PhoneNumber = +15075563221
def SendPhoneVerificationCode(studentName, studentPhone, code):
    try: 
        client = Client(account_SID, account_token)

        message = client.messages.create(
            body = f'Hello {studentName}, you requested to verify your phone number on the DHMS, Your verification code is: {code}.Thank you',
            from_ = twilio_phn,
            to = f'+234{studentPhone}'
        )
        print("SMS sent successfully. Message SID is :", message.sid)
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Verification SMS sent successfully"
        })
        
    except:
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "An error occured. Kindly try again"
        })