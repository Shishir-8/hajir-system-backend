
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # authentication urls
    path('api/auth/', include('accounts.urls')),
    path('api/employees/', include('employees.urls')),
    path('api/departments/', include('departments.urls')),
    path('api/attendance/', include('attendance.urls')),
]
