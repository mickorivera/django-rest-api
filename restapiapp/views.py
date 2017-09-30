from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import User
from .serializers import UserSerializer, RestrictedUserSerializer, UserStatusSerializer, \
    UserPasswordSerializer, UserDetailSerializer, RestrictedUserDetailSerializer
from .utils.auth_token import Generator as TokenGenerator,  Decoder as TokenDecoder
from .utils.email import Sender as EmailSender


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        user = serializer.save(password=password)
        token_generator = TokenGenerator()
        token = token_generator.generate(user)
        email_sender = EmailSender()
        email_sender.send('token = {}'.format(token), self.request.data['email'])

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

    def _extract_user_id(self, token):
        token_decoder = TokenDecoder()
        payload = token_decoder.decode(token)
        return payload.get('user_id')

    def patch(self, request, pk):
        user_id = self._extract_user_id(self.request.data.get('token'))
        if str(user_id) != str(pk):
            return Response({'token': ['token not valid']}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=pk)
        data = {'is_active': True}
        new_user = UserStatusSerializer(user, data=data, partial=True)
        if new_user.is_valid():
            new_user.save()
        return Response(new_user.data)


class UserPassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPasswordSerializer
    
    def perform_update(self, serializer):
        if self.request.user == serializer.instance:
            user = serializer.save()
        else:
            raise PermissionDenied
        