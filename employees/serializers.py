from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import Employee

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "role",
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    # Display user information in GET responses
    user = UserDetailSerializer(read_only=True)

    # Accept user information when creating an employee
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        trim_whitespace=False,
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "user",
            "email",
            "first_name",
            "last_name",
            "password",
            "department",
            "designation",
            "phone_number",
        ]
        read_only_fields = ["id", "user"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data.pop("email")
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        password = validated_data.pop("password")

        # Create the user account
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role="EMPLOYEE",
        )

        # Create the employee profile
        employee = Employee.objects.create(
            user=user,
            **validated_data,
        )

        return employee