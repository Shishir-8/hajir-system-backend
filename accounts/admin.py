from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['first_name', 'last_name', 'email', 'role', 'is_staff', 'is_superuser', 'is_active']
    list_display_links = ['first_name', 'last_name', 'email']
    list_filter = ['role', 'is_staff', 'is_active']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Fieldsets used when creating a user from the "+ Add User" button in admin
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role','is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    






