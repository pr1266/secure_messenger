from unicodedata import lookup
from urllib import response
from django.shortcuts import render
from rest_framework.generics import ListAPIView , RetrieveAPIView , CreateAPIView , UpdateAPIView , DestroyAPIView
from .models import *
from .permissions import *
from rest_framework import views, permissions
from .serializer import *
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes , api_view, throttle_classes
from django.http import JsonResponse , HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, get_user_model, logout
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import(
    AllowAny ,
    IsAuthenticated ,
    IsAdminUser ,
    IsAuthenticatedOrReadOnly ,
)
from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST
from django.core import serializers
from rest_framework.filters import(
    SearchFilter ,
    OrderingFilter ,
)
from rest_framework.decorators import authentication_classes, permission_classes

class UserListApiView(ListAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['id', 'username']

class UserCreateApiView(CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@throttle_classes([UserRateThrottle])
def get_my_contacts(request):
    print(request.data)
    username = request.data['username']
    obj = UserMessage.objects.filter(Q(sender__username = username)|Q(reciever__username = username))
    serialized_obj = UserMessageSerializer(obj, many = True)
    return Response(serialized_obj.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def is_admin(request):
    id = int(request.data['group'])        
    owner_ = Group.objects.filter(pk = id)        
    current_user = str(request.user)
    return Response(current_user == str(owner_.values_list('owner_id', flat = True)[0]))

class UserMessageCreateApiView(CreateAPIView):

    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
    permission_classes = [IsAuthenticated]

class GroupCreateApiView(CreateAPIView):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

class GroupPermissionCreateApiView(CreateAPIView):

    queryset = GroupPermission.objects.all()
    serializer_class = GroupPermissionSerializer
    permission_classes = [IsAuthenticated, GroupOwnerPermission]

class GetMyGroups(ListAPIView):

    serializer_class = GroupPermissionSerializer
    permission_classes = [IsAuthenticated,]
    model = GroupPermission

    def get_queryset(self):
        
        user_id = self.request.user
        queryset = self.model.objects.filter(user = user_id)
        return queryset

class GetGroupUsers(ListAPIView):

    serializer_class = GroupPermissionSerializer
    permission_classes = [IsAuthenticated, isGroupMember]
    model = GroupPermission

    def get_queryset(self):

        g_id = self.kwargs['group']
        return self.model.objects.filter(group = g_id)

class GetGroupMessages(ListAPIView):

    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated, haveBLPAccess, isGroupMember]
    model = GroupMessage
    
    def get_queryset(self):
        group_id = self.kwargs['group']
        obj = self.model.objects.filter(Q(group = group_id))
        return obj
    
class SendMessageGroup(CreateAPIView):

    serializer_class = GroupMessageSerializer
    permission_classes = [IsAuthenticated, haveBibaAccess, isGroupMember]
    model = GroupMessage

class MessageDeleteAPIView(DestroyAPIView):

    queryset = GroupMessage.objects.all()
    serializer_class =  GroupMessageSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    permission_classes = [IsAuthenticated]
