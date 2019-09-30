from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin,
)

import jwt #pip install pyjwt
from datetime import datetime


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class, by inhe-
    riting from BaseUserManager, get a lot of Django code to create a User. 

    """

    def create_user(self, username, email, password=None):
        """Create and return a user."""

        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """Create and return a user with superuser/admin permissions."""

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # USERNAME_FIELD define which field is used to signin
    USERNAME_FIELD = 'username'  # ''email'
    REQUIRED_FIELDS = ['email']  # ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property  # Decorator @property defines a dynamic property
    def token(self):
        """Dynamic property to generate a JSON Web Token."""

        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """Generates a JSON Web Token with user info and expiry date."""

        now = datetime.timestamp(datetime.utcnow())
        expiration = now + (60 * 60)  # 1 hour (3600 seconds)

        token = jwt.encode({
            'id': self.pk,
            'expiration': expiration
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

