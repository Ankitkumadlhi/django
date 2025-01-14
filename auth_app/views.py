from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from auth_app.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    UserLoginSerializer
    )
from rest_framework.response import Response
from django.contrib.auth import authenticate



# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password) 

        if user:
            refresh = RefreshToken.for_user(user)
            user_serialized = UserSerializer(user)   
            return Response({
                'user': user_serialized.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })                                                                
    
class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = UserSerializer(request.user)
        return Response({
            'message': 'Welcome to the dashboard',
            'user': user.data
        }, status=200)
