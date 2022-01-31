from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Group)
admin.site.register(GroupPermission)
admin.site.register(GroupMessage)
admin.site.register(UserMessage)