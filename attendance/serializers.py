from rest_framework import serializers
from .models import Attendance
from employees.models import Employee


class MyAttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.user.full_name", read_only=True)
    class Meta:
        model = Attendance
        fields = [
            'id',
            'employee_name',
            'date',
            'check_in',
            'check_out',
            'working_duration',
            'late_minutes',
            'status'
        ]

        read_only_fields = fields


class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    employee_name = serializers.CharField(source="employee.user.full_name", read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id',
            'employee',
            'employee_name',
            'date',
            'check_in',
            'check_out',
            'working_duration',
            'late_minutes',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = ['id', 'employee_name', 'working_duration', 'created_at', 'updated_at']