from django.contrib import admin
from .models import Employee

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'designation', 'department', 'employment_status']
    list_display_links = ['user']
    list_filter = ['department','employment_status']
    search_fields = ['user']

    ordering = ['id']
