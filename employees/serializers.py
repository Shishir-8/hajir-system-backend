from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from rest_framework import serializers

from departments.models import Department
from .models import Employee

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "role",
        ]

class EmployeeSerializer(serializers.ModelSerializer):
    # Display user information in GET responses
    user = UserDetailSerializer(read_only=True)
    
    # Accept user information during creation and update
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    # Password is required during creation only
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        trim_whitespace=False,
        validators=[validate_password],
    )

    # Admin can create EMPLOYEE or MANAGER
    role = serializers.ChoiceField(
        choices=["EMPLOYEE", "MANAGER"],
        write_only=True,
    )

    # Accept Department primary key
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "email",
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
            "user",
            "created_at",
            "updated_at",
        ]

    def validate_email(self, value):
        email = value.strip().lower()

        users = User.objects.filter(email__iexact=email)

        if self.instance:
            users = users.exclude(id=self.instance.user_id)

        if users.exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return email

    @transaction.atomic
    def create(self, validated_data):

        password = validated_data.pop("password", None)

        if not password:
            raise serializers.ValidationError({
                "password": "Password is required."
            })

        email = validated_data.pop("email")
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        role = validated_data.pop("role")

        # Create User account
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
        )

        # Create Employee profile
        employee = Employee.objects.create(
            user=user,
            **validated_data,
        )

        return employee

    @transaction.atomic
    def update(self, instance, validated_data):

        email = validated_data.pop("email", None)
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        role = validated_data.pop("role", None)

        user = instance.user

        if email is not None:
            user.email = email

        if first_name is not None:
            user.first_name = first_name

        if last_name is not None:
            user.last_name = last_name

        if role is not None:
            user.role = role

        user.save()

        # Update Employee fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance