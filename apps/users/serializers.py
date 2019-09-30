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

    id = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj): 
        return obj.pk

    admin = serializers.SerializerMethodField(read_only=True)

    def get_admin(self, obj): 
        return obj.is_staff

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
        # fields included in request or response
        fields = ['id', 'username', 'password', 'email', 'admin', 'token']

    def create(self, validated_data):
        # Use the User.objects.create_user() to create a new user.
        return User.objects.create_user(**validated_data)


class SigninSerializer(serializers.Serializer):
    """Authenticates a user & creates a token."""
    
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    email = serializers.CharField(max_length=255, read_only=True)
    admin = serializers.BooleanField(read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user = authenticated_user(data)

        return {
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'admin': user.is_staff,
            'token': user.token
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Handles serialization and deserialization of User objects."""
    
    id = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj): 
        return obj.pk

    admin = serializers.SerializerMethodField(read_only=True)

    def get_admin(self, obj): 
        return obj.is_staff

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
        fields = ('id', 'username', 'password', 'email', 'admin', 'is_active', 'url',)

        # Alternative to read_only=True, prefered
        # cause don't want to specify anything else
        # read_only_fields = ('token',)

    def get(self, instance):
        return instance

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