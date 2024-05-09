from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(ChatPrompts)
admin.site.register(AIChat_Room)
admin.site.register(AIResponsePrompt)