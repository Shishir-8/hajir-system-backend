from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomLoginSerializer

# Create your views here.

class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer


