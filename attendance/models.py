from django.db import models
from django.db.models import Q, F


class AttendanceStatus(models.TextChoices):
    PRESENT = "PRESENT", "Present"
    LATE = "LATE", "Late"
    HALF_DAY = "HALF_DAY", "Half Day"
    ABSENT = "ABSENT", "Absent"
    ON_LEAVE = "ON_LEAVE", "On Leave"
    HOLIDAY = "HOLIDAY", "Holiday"


class Attendance(models.Model):
    employee = models.ForeignKey("employees.Employee", on_delete=models.PROTECT, related_name="attendances")
    date = models.DateField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
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
    grace_period_minutes = models.PositiveIntegerField(default=15)
    half_day_hours = models.DecimalField(max_digits=4, decimal_places=2, default=3.5)
    early_departure_grace_minutes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Attendance Settings"