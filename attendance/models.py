from django.db import models
from django.db.models import Q, F


class AttendanceStatus(models.TextChoices):
    PRESENT = "PRESENT", "Present"
    LATE = "LATE", "Late"
    ABSENT = "ABSENT", "Absent"
    ON_LEAVE = "ON_LEAVE", "On Leave"
    HOLIDAY = "HOLIDAY", "Holiday"

class WorkingDayType(models.TextChoices):
    FULL_DAY = "FULL_DAY", "Full Day"
    HALF_DAY = "HALF_DAY", "Half Day"


class Attendance(models.Model):
    employee = models.ForeignKey("employees.Employee", on_delete=models.PROTECT, related_name="attendances")
    date = models.DateField()
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    working_duration = models.DurationField(null=True, blank=True)
    working_day_type = models.CharField(max_length=20, choices=WorkingDayType.choices, null=True, blank=True)
    late_minutes = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=AttendanceStatus.choices, default=AttendanceStatus.PRESENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(fields=["employee", "date"], name="unique_employee_attendance_per_day"),
            models.CheckConstraint(condition=Q(check_out__isnull=True) | Q(check_out__gte=F("check_in")), name="check_out_after_check_in"),
            models.CheckConstraint(condition=Q(status__in=AttendanceStatus.values), name="valid_attendance_status"),
        ]
        indexes = [
            models.Index(fields=["date"], name="attendance_date_idx"),
        ]

    def __str__(self):
        return f"{self.employee} - {self.date}"


class AttendanceSetting(models.Model):
    office_start_time = models.TimeField(default="10:00")
    office_end_time = models.TimeField(default="17:00")
    required_working_hours = models.DecimalField(max_digits=4, decimal_places=2, default=7.0)
    grace_period_minutes = models.PositiveIntegerField(default=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Attendance Settings"