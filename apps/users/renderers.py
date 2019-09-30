from rest_framework.renderers import JSONRenderer
import json


class GenericJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    data_namespace = 'data'

    def render(self, data, media_type=None, renderer_context=None):

        token = None

        # When data is a single object, look for errors or new token
        if not isinstance(data, list):

            # If view has thrown an error, data will contain an errors key
            errors = data.get('errors', None)
            if errors:
                self.data_namespace = 'errors'
                data = data['errors']
                # and default JSONRenderer should handle rendering.
                #return super(UserJSONRenderer, self).render(data)

            # When a token key is part of the response, it will be a byte object,
            # but byte objects don't serialize well so we need to decode it
            token = data.pop('token', None)
            if token and isinstance(token, bytes):
                token = token.decode('utf-8')

        # If no token generated (like in signup/ signin) resend request's one
        # TokenAuthentication provides on success the following credentials:
        # request.user: a Django User instance
        # request.auth: a rest_framework.authtoken.models.Token instance
        if not token and renderer_context['request'].auth:
            token = renderer_context['request'].auth

        # Render token and data (or errors) seperated
        return json.dumps({
            self.data_namespace: data,
            'token': token
        })


class UserJSONRenderer(GenericJSONRenderer):
    data_namespace = 'user'


class UsersJSONRenderer(GenericJSONRenderer):
    data_namespace = 'users'
