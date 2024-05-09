from django.db import models

# Create your models here.
class ChatPrompts(models.Model):
    userID = models.CharField(max_length= 300)
    prompts = models.CharField(max_length= 1000)
    chatroomID = models.CharField(max_length= 300)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return self.chatroomID


class AIResponsePrompt(models.Model):
    response = models.CharField(max_length=1000)
    chatroomID = models.CharField(max_length= 300)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return self.chatroomID
    
class AIChat_Room(models.Model):
    uniqueId = models.CharField(max_length=1000)
    companyID = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
    def __str__(self):
        return self.uniqueId