from pyexpat.errors import messages
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# TransferEmailNotification(request, senderEmail, senderFirstName, senderLastName, transferAmount, getReceiverAccountName, getReceiverBank, transferstatus, newStudentAccountBalance)

def TransferEmailNotification(request, senderEmail, senderFirstName, senderLastName, amountToTransfer, getReceiverAccountName, getReceiverBank, transferstatus, newStudentAccountBalance):
    recipient_list = [senderEmail, ]

    context = {'senderEmail': senderEmail, 'senderFirstName':senderFirstName, 'senderLastName':senderLastName, 'amountToTransfer':amountToTransfer, 
               'getReceiverAccountName':getReceiverAccountName, 'getReceiverBank':getReceiverBank, 'transferstatus':transferstatus,
               'newStudentAccountBalance':newStudentAccountBalance,
               }
    html_message = render_to_string("mailouts/transferemail.html", context=context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject = "TRANSACTION NOTIFICATION ON THE DHMS.", 
        body = plain_message,
        from_email = 'dhmsinventoryapp@gmail.com',
        to= recipient_list
        )

    message.attach_alternative(html_message, "text/html")
    message.send()

    if message:
        print('Sent a login notification email')
    else:
        messages.error(request, f'Problem sending transfer notification email to {senderEmail}.')


