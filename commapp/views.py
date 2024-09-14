from django.shortcuts import render
import uuid
# from getstream.models.call_request import CallRequest
from getstream.models import (
    CallRequest,
    MemberRequest,
)
from getstream.models import UserRequest

# Create your views here.


def CommDashboard(request):
    return render(request, 'comm/dashboard.html')


def StartAudioCall(request):        
    # call = client.video.call("default", uuid.uuid4())
    # call.create(
    #     data=CallRequest(
    #         created_by_id="sacha",
    #     ),
    # )
    return render(request, 'comm/dashboard.html')

