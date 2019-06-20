from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth.models import User
from rest_framework import routers
from authentication.viewsets import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('', include('authentication.urls')),
    path('', include('mailservice.urls')),
    url(r'^api/token/$', TokenObtainPairView.as_view()),
    url(r'^api/token/refresh/$', TokenRefreshView.as_view()),
    url(r'^api/token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
]
