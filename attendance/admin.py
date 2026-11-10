from django.contrib import admin
from .models import Attendance, AttendanceSetting

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["id", "employee", "date", "check_in", "check_out", 'late_minutes', "status"]
    list_display_links = ['id', 'employee']
    list_filter = ["status", "date"]
    search_fields = ["employee__user__first_name", "employee__user__last_name", "employee__user__email"]

@admin.register(AttendanceSetting)
class AttendanceSettingsAdmin(admin.ModelAdmin):
    list_display = ["id", "office_start_time", "office_end_time", "grace_period_minutes", "required_working_hours"]