from django.urls import path

from .views import (
    SignupAPIView, 
    SigninAPIView,
    CurrentUserAPIView, 
    UserByIdAPIView,
    UsersListAPIView,
    AdminUsersListAPIView,
    NoAdminUsersListAPIView,
    ActiveUsersListAPIView,
    NoActiveUsersListAPIView,
)

app_name = 'users'

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'), # POST
    path('signin/', SigninAPIView.as_view(), name='signin'),  # POST
    path('current/', CurrentUserAPIView.as_view(), name='current'),  # POST, GET, PATCH, DELETE
    path('byid/<int:id>/', UserByIdAPIView.as_view(), name='byid'),  # POST, GET, PATCH, DELETE
    path('list/', UsersListAPIView.as_view(), name='list'), # GET
    path('admin-list/', AdminUsersListAPIView.as_view(), name='admin-list'), # GET
    path('no-admin-list/', NoAdminUsersListAPIView.as_view(), name='no-admin-list'), # GET
    path('active-list/', ActiveUsersListAPIView.as_view(), name='active-list'), # GET
    path('no-active-list/', NoActiveUsersListAPIView.as_view(), name='no-active-list'), # GET
]