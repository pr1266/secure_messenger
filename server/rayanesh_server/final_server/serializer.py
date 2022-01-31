from .models import *
from rest_framework.serializers import ModelSerializer , SerializerMethodField , CharField , ValidationError , StringRelatedField
from django.db.models import Q

class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'

class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"

class GroupPermissionSerializer(ModelSerializer):

    class Meta:
        model = GroupPermission
        fields = "__all__"

class GroupMessageSerializer(ModelSerializer):

    class Meta:
        model = GroupMessage
        fields = '__all__'

class UserMessageSerializer(ModelSerializer):

    class Meta:
        model = UserMessage
        fields = '__all__'