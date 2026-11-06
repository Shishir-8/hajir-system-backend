from django.contrib import admin
from .models import Department

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','is_active', 'created_at']
    list_display_links = ['id', 'name']
    search_fields = ['name']

    ordering = ['id']
