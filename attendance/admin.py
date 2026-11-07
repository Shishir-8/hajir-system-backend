from django.contrib import admin
from .models import Attendance, AttendanceSetting

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["id", "employee", "date", "check_in", "check_out", "status"]
    list_filter = ["status", "date"]
    search_fields = ["employee__user__first_name", "employee__user__last_name", "employee__user__email"]

@admin.register(AttendanceSetting)
class AttendanceSettingsAdmin(admin.ModelAdmin):
    list_display = ["id", "office_start_time", "office_end_time", "grace_period_minutes", "half_day_hours"]