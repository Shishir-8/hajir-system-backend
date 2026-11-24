from datetime import timedelta
from rest_framework import serializers
from .models import Leave


class LeaveSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source="employee.user.full_name",
        read_only=True,
    )

    number_of_days = serializers.IntegerField(
        min_value=1,
        write_only=True,
    )

    class Meta:
        model = Leave
        fields = [
            "id",
            "employee",
            "employee_name",
            "number_of_days",
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "status",
            "reviewed_by",
            "reviewed_at",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "employee",
            "end_date",
            "status",
            "reviewed_by",
            "reviewed_at",
            "created_at",
        ]

    def create(self, validated_data):
        number_of_days = validated_data.pop("number_of_days")

        validated_data["end_date"] = (
            validated_data["start_date"]
            + timedelta(days=number_of_days - 1)
        )

        return Leave.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["number_of_days"] = instance.number_of_days
        return data