from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView

from django.shortcuts import get_object_or_404

from .models import User
from .serializers import SignupSerializer, SigninSerializer, UserSerializer
from .renderers import UserJSONRenderer, UsersJSONRenderer


class SignupAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)  # create serializer
        serializer.is_valid(raise_exception=True)  # validate serializer
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SigninAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SigninSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    renderer_classes = (UserJSONRenderer,)

    def get_queryset(self, request):
        return request.user

    def retrieve(self, request, *args, **kwargs):
        user = self.get_queryset(request)

        serializer = self.serializer_class(
            user, 
            context={'request': request}  # required by url field
        )  
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = self.get_queryset(request)
        data = request.data.get('user', {})

        serializer = self.serializer_class(
            user, 
            data=data, 
            partial=True,
            context={'request': request}  # required by url field
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        user = self.get_queryset(request)
        data = request.data.get('user', {})

        serializer = self.serializer_class(user, data=data)
        serializer.delete()

        return Response({}, status=status.HTTP_200_OK)


class UserByIdAPIView(CurrentUserAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    renderer_classes = (UserJSONRenderer,)

    def get_queryset(self, request):
        return get_object_or_404(User, pk=self.kwargs['id'])


class UsersListAPIView(RetrieveAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    renderer_classes = (UsersJSONRenderer,)

    def get_queryset(self):
        return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.serializer_class(
            queryset,
            many=True,
            context={'request': request}  # required by url field
        )  

        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminUsersListAPIView(UsersListAPIView):

    def get_queryset(self):
        return User.objects.filter(is_staff=True)


class NoAdminUsersListAPIView(UsersListAPIView):

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class ActiveUsersListAPIView(UsersListAPIView):

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class NoActiveUsersListAPIView(UsersListAPIView):

    def get_queryset(self):
        return User.objects.filter(is_active=False)
