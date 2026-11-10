from django.contrib import admin
from .models import Employee

# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'designation', 'department', 'employment_status']
    list_display_links = ['first_name']
    list_filter = ['department', 'employment_status']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    ordering = ['id']

    @admin.display(description='First Name')
    def first_name(self, obj):
        return obj.user.first_name

    @admin.display(description='Last Name')
    def last_name(self, obj):
        return obj.user.last_name