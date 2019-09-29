from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User


def authenticated_user(data):
    """Authentication process."""

    username = data.get('username', None)
    password = data.get('password', None)

    if username is None:
        raise serializers.ValidationError(
            'A username is required to log in.'
        )

    if password is None:
        raise serializers.ValidationError(
            'A password is required to log in.'
        )

    user = authenticate(username=username, password=password)

    if user is None:
        raise serializers.ValidationError(
            'A user with this username and password was not found.'
        )

    if not user.is_active:
        raise serializers.ValidationError(
            'This user has been deactivated.'
        )

    return user


class SignupSerializer(serializers.ModelSerializer):
    """Requests and creates a new user."""

    # Set passwords between 4-128 chars and can not be read by the client
    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True
    )

    # Client should not be able to send a token along with a registration
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # fields that could possibly included in a request or response
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Use the User.objects.create_user() to create a new user.
        return User.objects.create_user(**validated_data)


class SigninSerializer(serializers.Serializer):
    """Authenticates a user & creates a token"""
    
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user = authenticated_user(data)

        return {
            'username': user.username,
            'email': user.email,
            'token': user.token
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True
    )

    url = serializers.HyperlinkedIdentityField(
        view_name='users:byid',
        lookup_field='id',
        read_only=True, 
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'url',)

        # Alternative to read_only=True, prefered
        # cause don't want to specify anything else
        # read_only_fields = ('token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

    def delete(self):
        user = authenticated_user(self.initial_data)
        user.delete()

        return None