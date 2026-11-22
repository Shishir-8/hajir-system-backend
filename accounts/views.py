from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomLoginSerializer, ChangePasswordSerializer, ForgetPasswordSerializer, ResetPasswordSerializer, MyProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Password has been updated successfully."
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message':"Logout succesfully"},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {'message':"Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

class MyProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = MyProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'If an account exists with this email, a password reset link has been sent.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Password reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
    
    
        









