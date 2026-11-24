from django.contrib import admin
from .models import Leave

# Register your models here.

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'leave_type','reason', 'status']
    list_display_links = ['id', 'employee']
    list_filter = ['leave_type']

