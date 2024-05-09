from django.urls import path
from . import views


urlpatterns = [
    path('', views.StartChat, name="StartChat"),
    path('sendprompt', views.Send, name="Send"),
    path('getprompt/<str:chatroomID>', views.GetResponse, name="GetResponse"),
    # path('chatpage', views.AiChatPage, name="AiChatPage"),
    path('chatpage', views.AiChatPage, name="AiChatPage"),
]

