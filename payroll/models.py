from decimal import Decimal
from django.db import models
from employees.models import Employee


class EmployeeSalary(models.Model):
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="salary"
    )

    basic_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    allowance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee} - {self.basic_salary}"



class PayrollStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"


class Payroll(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="payrolls"
    )

    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()

    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    allowance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )
    deduction = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

    net_salary = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=10,
        choices=PayrollStatus.choices,
        default=PayrollStatus.PENDING
    )

    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "-month"]
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "month", "year"],
                name="unique_employee_payroll_per_month"
            )
        ]

    def __str__(self):
        return f"{self.employee} - {self.month}/{self.year}"