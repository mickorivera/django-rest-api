import jwt
from rest_framework_jwt.settings import api_settings


class Generator:
    def __init__(self):
        self._jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        self._jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    def generate(self, user):
        payload = self._jwt_payload_handler(user)
        token = self._jwt_encode_handler(payload)
        return token

class Decoder:
    def __init__(self):
        self._jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

    def decode(self, token):
        # try:
            # payload = self._jwt_decode_handler(token)
        # except jwt.ExpiredSignature:
        #     msg = _('Signature has expired.')
        #     # raise exceptions.AuthenticationFailed(msg)
        # except jwt.DecodeError:
        #     msg = _('Error decoding signature.')
            # raise exceptions.AuthenticationFailed(msg)
        # except jwt.InvalidTokenError:
            # raise exceptions.AuthenticationFailed()

        # return payload
        return self._jwt_decode_handler(token)
        