from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from rest_framework import serializers

from departments.models import Department
from .models import Employee

User = get_user_model()


class EmployeeSerializer(serializers.ModelSerializer):

    # Access User fields using source
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        trim_whitespace=False,
        validators=[validate_password],
    )
    role = serializers.ChoiceField(
        source="user.role",
        choices=["EMPLOYEE", "MANAGER"],
        write_only=True,
        required=False,
    )

    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "role",
            "department",
            "designation",
            "phone_number",
            "address",
            "joining_date",
            "employment_status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_email(self, value):
        email = value.strip().lower()

        users = User.objects.filter(email__iexact=email)

        if self.instance:
            users = users.exclude(pk=self.instance.user_id)

        if users.exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return email

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = validated_data.pop("password", None)

        if not password:
            raise serializers.ValidationError({
                "password": "Password is required."
            })

        role = user_data.pop("role", None)

        if not role:
            raise serializers.ValidationError({
                "role": "Role is required."
            })

        user = User.objects.create_user(
            email=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            password=password,
            role=role,
        )

        employee = Employee.objects.create(
            user=user,
            **validated_data,
        )

        return employee

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        # Ignore password during profile updates
        validated_data.pop("password", None)
        user = instance.user

        for attr, value in user_data.items():
            setattr(user, attr, value)

        if user_data:
            user.save()

        return super().update(instance, validated_data)