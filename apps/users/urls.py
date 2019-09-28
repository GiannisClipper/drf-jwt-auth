from django.urls import path

from .views import SignupAPIView, SigninAPIView, UpdateCurrentUserAPIView

app_name = 'authentication'

urlpatterns = [
    path('signup/', SignupAPIView.as_view()),
    path('signin/', SigninAPIView.as_view()),
    path('update_current/', UpdateCurrentUserAPIView.as_view()),
]