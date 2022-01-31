from django.db import models
from django_bleach.models import BleachField

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):

    username = models.CharField(max_length = 250, primary_key = True)
    password = models.CharField(max_length = 250, null = False)

    USERNAME_FIELD = 'username'

    def __str__(self):

        return self.username

class Group(models.Model):

    owner = models.ForeignKey(CustomUser, on_delete = models.CASCADE)

    def __str__(self):

        return str(self.id)

class GroupPermission(models.Model):

    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    biba = models.BooleanField(default = False)
    blp = models.BooleanField(default = False)
    delete_permission = models.BooleanField(default = False)
    
    class Meta:
        unique_together = (("group", "user"),)

class GroupMessage(models.Model):

    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    message = BleachField(max_length = 250, null = True)

class UserMessage(models.Model):

    sender = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = 'sender')
    reciever = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name = 'reciever')
    content = BleachField(max_length = 250, null = True)