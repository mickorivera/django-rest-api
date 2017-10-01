from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserViewSet

urlpatterns = format_suffix_patterns([
    url(r'^user/$',
        UserViewSet.as_view({
                'post': 'create',
                'get': 'list'
            }),
        name='user-list'),

    url(r'^user/(?P<pk>[0-9]+)/$',
        UserViewSet.as_view({
                'get': 'retrieve',
                'patch': 'partial_update'
            }),
        name='user-detail'),

    url(r'^user/(?P<pk>[0-9]+)/is_active/$',
        UserViewSet.as_view({
                'patch': 'activate'
            }),
        name='user-status'),

])