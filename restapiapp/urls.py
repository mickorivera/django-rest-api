from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserList, UserStatus, UserPassword, UserDetail

urlpatterns = format_suffix_patterns([
    url(r'^users/$',
        UserList.as_view(),
        name='user-list'),

    url(r'^user/status/(?P<token>.+?)/$',
        UserStatus.as_view(),
        name='user-status'),

    url(r'^users/(?P<pk>[0-9]+)/password/$',
        UserPassword.as_view(),
        name='user-password'),
    
    url(r'^users/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(),
        name='user-detail'),
])