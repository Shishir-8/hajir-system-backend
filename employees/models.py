from django.db import models
from django.conf import settings

# Create your models here.

class DepartmentChoices(models.TextChoices):
    IT = "IT", "Information Technology"
    HR = "HR", "Human Resources"
    FINANCE = "FINANCE", "Finance"

class DesignationChoices(models.TextChoices):
    CEO = "CEO", "Chief Executive Officer"
    CTO = "CTO", "Chief Technology Officer"
    MANAGER = "MANAGER", "Manager"
    HR_MANAGER = "HR_MANAGER", "HR Manager"
    ACCOUNTANT = "ACCOUNTANT", "Accountant"
    SOFTWARE_DEVELOPER = "SOFTWARE_DEVELOPER", "Software Developer"
    BACKEND_DEVELOPER = "BACKEND_DEVELOPER", "Backend Developer"
    FRONTEND_DEVELOPER = "FRONTEND_DEVELOPER", "Frontend Developer"
    UI_UX_DESIGNER = "UI_UX_DESIGNER", "UI/UX Designer"
    QA_ENGINEER = "QA_ENGINEER", "QA Engineer"
    SALES_EXECUTIVE = "SALES_EXECUTIVE", "Sales Executive"
    MARKETING_EXECUTIVE = "MARKETING_EXECUTIVE", "Marketing Executive"
    SUPPORT_EXECUTIVE = "SUPPORT_EXECUTIVE", "Support Executive"
    INTERN = "INTERN", "Intern"
    OTHER = "OTHER", "Other"


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.CharField(max_length=50, choices=DepartmentChoices.choices)
    designation = models.CharField(max_length=100, choices=DesignationChoices.choices)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_joining = models.DateTimeField()

    def __str__(self):
        return f"{self.user.first_name} - {self.user.email}"