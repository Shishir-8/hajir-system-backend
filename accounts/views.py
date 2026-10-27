from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomLoginSerializer, RegisterSerializer, PasswordResetSerializer, ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered Succesfully",
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer


class PasswordResetRequestView(APIView):

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()

            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = f"https://yourfrontend.com/reset-password?uid={uid}&token={token}"

            subject = "Password Reset Request"
            message = (
                f"Hello {user.first_name},\n\n"
                f"You requested a password reset for your account. "
                f"Please click the link below to set a new password:\n\n"
                f"{reset_url}\n\n"
                f"If you did not request this, please ignore this email.\n"
                f"The link will expire shortly."
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[email],
                fail_silently= False,
                using="default"
            )

            return Response({
                "message": "If an account exists for that email, a password-reset link will be sent.",
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Password has been reset successfully. You can now log in."
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









