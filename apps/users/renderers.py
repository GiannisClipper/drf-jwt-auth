from rest_framework.renderers import JSONRenderer
import json


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        # If view throws an error, data will contain an errors key
        # and default JSONRenderer should handle rendering.
        errors = data.get('errors', None)
        if errors is not None:
            return super(UserJSONRenderer, self).render(data)

        # If a token key is part of the response, it will be a byte object,
        # but byte objects don't serialize well so we need to decode it.
        token = data.get('token', None)
        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        # Render data under user namespace.
        return json.dumps({
            'user': data
        })