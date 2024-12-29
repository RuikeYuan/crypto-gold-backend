
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from backend import settings

class Thread(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=500, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)




