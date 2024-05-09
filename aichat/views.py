from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from aichat.models import AIChat_Room, AIResponsePrompt, ChatPrompts
from django.utils.crypto import get_random_string
import google.generativeai as genai
GOOGLE_API_KEY = "AIzaSyAFRclj4efF46KJVAaAocVeBlFPyYRTKGA"
import re
from django.contrib.auth.decorators import login_required

# Create your views here.

def replace_with_bold(text):
    return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

@login_required(login_url='Login')
def Send(request):
    # print('post request incoming')
    message = request.POST['message']
    username = request.POST['username']
    chatroomID = request.POST['chatroomID']
    new_prompt = ChatPrompts.objects.create(userID = request.user.last_name, prompts = message, chatroomID = chatroomID)
    new_prompt.save()

    # AI prompt config starts here
    model = genai.GenerativeModel('models/gemini-pro')
    genai.configure(api_key = GOOGLE_API_KEY)
    resp = model.generate_content(message)

    # AI Response starts here
    itemtoremove = '*'
    mainResponse = resp.text

    # sentence = "Replace **this text** with bold formatting."
    formatted_sentence = replace_with_bold(mainResponse)
    print(formatted_sentence)

    mainResponseToSave = formatted_sentence.replace(itemtoremove, "\n\n\n\n")
    AIResponsePromptSave = ChatPrompts.objects.create(userID = 'AI', prompts = mainResponseToSave, chatroomID = chatroomID)
    AIResponsePromptSave.save()
    return HttpResponse('message delivered.')


@login_required(login_url='Login')
def AiChatPage(request):
    latestRoomIDMain = AIChat_Room.objects.filter(companyID = request.user.last_name).first
    context = {'latestRoomIDMain':latestRoomIDMain}
    return render(request, 'aichat/chatroom.html', context)


@login_required(login_url='Login')
def StartChat(request):
    if request.method == 'POST':
        uniqueId = 'AI_Chat-' + get_random_string(length=10)
        createAIChat_Room = AIChat_Room.objects.create(uniqueId = uniqueId, companyID = request.user.last_name)
        createAIChat_Room.save()
        if createAIChat_Room:
            return redirect('AiChatPage')
    return render(request, 'aichat/startchat.html')


def GetResponse(request, chatroomID):
    chatID = ChatPrompts.objects.filter(chatroomID = chatroomID)
    # print(chatID)
    # airesponse = AIResponsePrompt.objects.filter(chatroomID = chatroomID)
    return JsonResponse({"messages":list(chatID.values())})


