from rest_framework.response import Response
from django.contrib.auth.models import User

from useronboard.models import AccountValidation


def ActivateUserBeforeRegister(email, code):
    findUserAccountValidation = AccountValidation.objects.filter(useremail=email).first()

    if findUserAccountValidation:
        return Response({
                    "status": 200,
                    "message": "Account has already been activated.",
                })

    else:
        findUser = User.objects.get(email=email).first()
        if findUser:
            CreateAccountValidation = AccountValidation(useremail = email, accountValidationCode = code, activationStatus = 'verified')
            CreateAccountValidation.save()
            Response({
                        "status": 200,
                        "message": "Student profile created successfull.",
                        "response": 'Account activated for user: ' + email 
                    })
            if code != '1234':
                return Response({
                            "status": 404,
                            "message": "Incorrect code.",
                            "response": 'Account activation failed for user: ' + email 
                        })
            else: return Response({
                            "status": 200,
                            "message": "Student profile created successfull.",
                            "response": 'Account activated for user: ' + email 
                        })
        else: return Response({
                        "status": 200,
                        "message": "Student profile created successfull.",
                        "response": 'Account activated for user: ' + email 
                    })

