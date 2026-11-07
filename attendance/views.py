from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from employees.models import Employee
from .models import Attendance, AttendanceSetting, AttendanceStatus
from rest_framework import status
from django.db import IntegrityError, transaction

# Create your views here.

class CheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        employee = Employee.objects.filter(user=request.user).first()

        if not employee:
            return Response({'message':'Employee profile not found',}, status=status.HTTP_404_NOT_FOUND)
        
        if employee.employment_status != "ACTIVE":
            return Response({'message':'Your employee account is not active'}, status=status.HTTP_403_FORBIDDEN)

        settings = AttendanceSetting.objects.all()
        if not settings:
            return Response({'message':"Attendance settings are not configured"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        now = timezone.now()
        local_now = timezone.localtime.now()
        today = local_now.date()

        if Attendance.objects.filter(employee=employee, date=today).exists():
            return Response({'message':'You have already check in today'}, status=status.HTTP_400_BAD_REQUEST)

        office_start = datetime.combine(today, settings.office_start_time)
        office_start = timezone.make_aware(office_start, timezone.get_current_timezone())
        late_after = office_start + timedelta(minutes=settings.grace_period_minutes)

        if now > late_after:
            attendance_status = AttendanceStatus.LATE
        else:
            attendance_status = AttendanceStatus.PRESENT

        try:
            with transaction.atomic():
                attendance = Attendance.objects.create(
                    employee=employee,
                    date = today,
                    check_in=now,
                    status = attendance_status
                )
        except IntegrityError:
            return Response({'message':"You have already checked in today"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message':"Check-in succesfully",
            "data":{
                "id": attendance.id,
                "date": attendance.date,
                "check_in": attendance.check_in,
                "status": attendance.status
            }
        }, status=status.HTTP_201_CREATED)






        

        
