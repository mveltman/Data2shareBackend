from rest_framework import viewsets, permissions, generics
from django.core import serializers
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class UserDetail(viewsets.ViewSet):
    serializer_class = UserSerializer
    queryset = ''

    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        print("test")
        print(request.data)
        user = authenticate(
            username=self.request.data["username"],
            password=self.request.data["password"])
        if(user is not None):
            data = model_to_dict(user)
            return Response(data)
        return Response("error")
        # works but sends the entire user (probably dont want that)


class UserCreate(viewsets.ViewSet):
    serializer_class = UserSerializer
    queryset = ''

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        user = User.objects.create_user(
            self.request.data["username"],
            self.request.data["email"],
            self.request.data["password"])
        if(user is not None):
            data = model_to_dict(user)
            return Response(data)
        return Response("error: unable to create user")
