from django.contrib import admin
from .models import Employee

# Register your models here.
@admin.register(Employee)
class CustomEmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'department', 'designation']
    list_display_links = ['id', 'user']
    search_fields = ['user']
    list_filter = ['department', 'designation']
