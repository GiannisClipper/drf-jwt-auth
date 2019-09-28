from django.urls import path

from .views import SignupAPIView, SigninAPIView, CurrentUserAPIView

app_name = 'authentication'

urlpatterns = [
    path('signup/', SignupAPIView.as_view()), # POST
    path('signin/', SigninAPIView.as_view()),  # POST
    path('current/', CurrentUserAPIView.as_view()),  # POST, GET, PATCH, DELETE
]