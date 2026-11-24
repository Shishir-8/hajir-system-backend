
from django.conf import settings
from django.db import models
from django.db.models import Q, F


class LeaveType(models.TextChoices):
    CASUAL = "CASUAL", "Casual Leave"
    SICK = "SICK", "Sick Leave"
    ANNUAL = "ANNUAL", "Annual Leave"
    UNPAID = "UNPAID", "Unpaid Leave"
    OTHER = "OTHER", "Other"


class LeaveStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    CANCELLED = "CANCELLED", "Cancelled"


class Leave(models.Model):
    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.PROTECT,
        related_name="leaves"
    )

    leave_type = models.CharField(
        max_length=20,
        choices=LeaveType.choices
    )

    start_date = models.DateField()
    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=LeaveStatus.choices,
        default=LeaveStatus.PENDING
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_leaves"
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.CheckConstraint(
                condition=Q(end_date__gte=F("start_date")),
                name="leave_end_date_after_start_date"
            )
        ]

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"
    

    @property
    def number_of_days(self):
        return (self.end_date - self.start_date).days + 1
