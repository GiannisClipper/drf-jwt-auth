from django.conf import settings
from rest_framework import authentication, exceptions

import jwt #pip install pyjwt
from datetime import datetime

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) != 2:
            return None

        # Prefix & token have to be docoded, 
        # cause JWT library can't handle the byte type
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != self.authentication_header_prefix.lower():
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        now = datetime.timestamp(datetime.utcnow())
        expiration = now + (60 * 60)  # 1 hour (3600 seconds)
        if payload['expiration'] + (60 * 60) < now:
            msg = 'Authentication token has been expired.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)