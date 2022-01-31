from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from django.conf import settings
from django.contrib.auth import views as auth_views
from final_server import views

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('secret/', admin.site.urls),
    url(r'api-token-auth/' , obtain_jwt_token),
    url('createuser/', views.UserCreateApiView.as_view()),
    url('send_message/', views.UserMessageCreateApiView.as_view()),
    url('get_my_contact/', views.get_my_contacts),
    url('creategroup/', views.GroupCreateApiView.as_view()),
    url('add_to_group/', views.GroupPermissionCreateApiView.as_view()),
    url(r'get_group_users/(?P<group>[\w-]+)/$', views.GetGroupUsers.as_view()),
    url('my_groups/', views.GetMyGroups.as_view()),
    url('send_group_message/', views.SendMessageGroup.as_view()),
    url(r'get_group_message/(?P<group>[\w-]+)/$', views.GetGroupMessages.as_view()),
    url('is_admin/', views.is_admin),
    url(r'^group_message/(?P<id>[\w-]+)/delete/$' , views.MessageDeleteAPIView.as_view() , name = 'delete'),
]


