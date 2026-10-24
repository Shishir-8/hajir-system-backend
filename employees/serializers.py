from rest_framework import serializers
from .models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role']


class EmployeeSerializer(serializers.ModelSerializer):
    user = EmployeeUserSerializer(read_only=True)
    class Meta:
        model = Employee
        fields = ('id', 'user', 'department', 'designation', 'phone_number')
