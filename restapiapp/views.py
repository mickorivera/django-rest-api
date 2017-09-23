from django.core.exceptions import PermissionDenied
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, RestrictedUserSerializer, UserStatusSerializer, \
    UserPasswordSerializer, UserDetailSerializer, RestrictedUserDetailSerializer
from .utils.auth_token import Generator as TokenGenerator,  Decoder as TokenDecoder


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
    	user = serializer.save()
    	token_generator = TokenGenerator()
    	token = token_generator.generate(user)
    	print(token) # TODO: send this to user email address

    def get_serializer_class(self):
        if self.request.user.is_authenticated():
            return UserSerializer
        return RestrictedUserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.AllowAny, )  

    def get_serializer_class(self):
        if self.request.user.is_authenticated():
            return UserDetailSerializer
        return RestrictedUserDetailSerializer


class UserStatus(generics.UpdateAPIView):
    permission_classes = (permissions.AllowAny, )

    def _get_object(self, id):
        return User.objects.get(id=id)

    def patch(self, request, *args, **kwargs):
        print(request.auth)
        token = kwargs.pop('token')
        token_decoder = TokenDecoder()
        payload = token_decoder.decode(token)

        user = self._get_object(id=payload.get('user_id'))
        new_user = UserStatusSerializer(user, data=request.data, partial=True)
        if new_user.is_valid():
            new_user.save()
            return Response(new_user.data)
        else:
            return Response("wrong parameters")


class UserPassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPasswordSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def perform_update(self, serializer):
        if self.request.user == serializer.instance:
            user = serializer.save()
        else:
            raise PermissionDenied
        