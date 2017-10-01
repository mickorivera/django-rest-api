from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from .models import User
from .serializers import UserSerializer, RestrictedUserSerializer, UserStatusSerializer
from .utils.auth_token import Generator as TokenGenerator,  Decoder as TokenDecoder
from .utils.email import Sender as EmailSender
from .permissions import IsSelf


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, IsSelf)

    def perform_create(self, serializer):
        user = serializer.save()
        self._send_token(user)

    @detail_route(methods=['patch'])
    def activate(self, request, pk):
        user_id = self._extract_user_id(self.request.data.get('token'))
        if str(user_id) != str(pk):
            return Response({'token': ['token not valid']}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=pk)
        data = {'is_active': True}
        new_user = UserStatusSerializer(user, data=data, partial=True)
        if new_user.is_valid():
            new_user.save()
        return Response(new_user.data)

    def get_serializer_class(self):
        if self.request.user.is_authenticated():
            return UserSerializer
        return RestrictedUserSerializer

    def _send_token(self, user):
        token_generator = TokenGenerator()
        token = token_generator.generate(user)
        email_sender = EmailSender()
        email_sender.send('token = {}'.format(token), self.request.data['email'])

    def _extract_user_id(self, token):
        token_decoder = TokenDecoder()
        payload = token_decoder.decode(token)
        return payload.get('user_id')
