from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from employees.models import Employee


User = get_user_model()

# login serializer
class CustomLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data['message'] = "Login Succesfull"
        data['user'] = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role
        }
        data['permissions'] = sorted(user.get_all_permissions())
       
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is invalid")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "Passwords do not match"
            })

        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({
                'new_password': "New password must be different"
            })
        
        return data 

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def save(self):
        email = self.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return 

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
        send_mail(
            subject="Reset your password",
            message=(
                f"Hello {user.first_name},\n\n"
                f"Click the link below to reset your password:\n"
                f"{reset_link}\n\n"
                "If you did not request this, ignore this email."
            ),
            from_email= settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password':'Passwords do not match'})

        try:
            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            raise serializers.ValidationError({"uid":"Invalid reset link"})

        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError({'token':"Invalid token or expired reset token."})

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class MyProfileSerializer(serializers.ModelSerializer):

    phone_number = serializers.CharField(
        source="employee_profile.phone_number",
        read_only=True
    )

    address = serializers.CharField(
        source="employee_profile.address",
        read_only=True
    )

    designation = serializers.CharField(
        source="employee_profile.designation",
        read_only=True
    )

    joining_date = serializers.DateField(
        source="employee_profile.joining_date",
        read_only=True
    )

    employment_status = serializers.CharField(
        source="employee_profile.employment_status",
        read_only=True
    )

    department= serializers.CharField(
        source="employee_profile.department.name",
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "phone_number",
            "address",
            "designation",
            "department",
            "joining_date",
            "employment_status",
        ]




            

            

    