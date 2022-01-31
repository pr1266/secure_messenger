from rest_framework import permissions
from .models import *
from django.db.models import Q

class GroupOwnerPermission(permissions.BasePermission):

    message = "you are not owner of group"
    
    def has_permission(self, request, view):
        id = int(request.data['group'])        
        owner_ = Group.objects.filter(pk = id)        
        current_user = str(request.user)
        return current_user == str(owner_.values_list('owner_id', flat = True)[0])
        
class haveBibaAccess(permissions.BasePermission):

    message = "you dont have biba access"

    def has_permission(self, request, view):

        current_user = str(request.user)
        perm = GroupPermission.objects.filter(Q(group = request.data['group']) & Q(user = request.user))
        perm = perm.values_list('biba', flat = True)[0]
        return bool(perm)

class haveBLPAccess(permissions.BasePermission):

    message = 'you dont have blp access'

    def has_permission(self, request, view):

        current_user = str(request.user)
        perm = GroupPermission.objects.filter(Q(group = view.kwargs['group']) & Q(user = request.user))
        perm = perm.values_list('blp', flat = True)[0]
        print(perm)

        return bool(perm)

class isGroupMember(permissions.BasePermission):

    message = 'you are not member of group'

    def has_permission(self, request, view):
        print('checked')
        g_id = None
        if 'group' in view.kwargs.keys():

            g_id = view.kwargs['group']
        else:
            g_id = request.data['group']
            
        obj = GroupPermission.objects.filter(Q(group = g_id) & Q(user = request.user))
        if len(obj) == 0:
            return False
        return True