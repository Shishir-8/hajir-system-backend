from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from employees.models import Employee
from .models import Attendance, AttendanceSetting, AttendanceStatus, WorkingDayType
from rest_framework import status
from django.db import IntegrityError, transaction
from .serializers import MyAttendanceSerializer, AttendanceSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from accounts.permissions import IsAdmin, IsAdminOrManager
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.

class CheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        employee = Employee.objects.filter(user=request.user).first()

        if not employee:
            return Response({'message':'Employee profile not found',}, status=status.HTTP_404_NOT_FOUND)
        
        if employee.employment_status != "ACTIVE":
            return Response({'message':'Your employee account is not active'}, status=status.HTTP_403_FORBIDDEN)

        settings = AttendanceSetting.objects.first()
        if not settings:
            return Response({'message':"Attendance settings are not configured"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        now = timezone.now()
        local_now = timezone.localtime()
        today_date = timezone.localdate()

        if Attendance.objects.filter(employee=employee, date=today_date).exists():
            return Response({'message':'You have already check in today'}, status=status.HTTP_400_BAD_REQUEST)

        office_start = datetime.combine(today_date, settings.office_start_time)
        office_start = timezone.make_aware(office_start, timezone.get_current_timezone())
        late_after = office_start + timedelta(minutes=settings.grace_period_minutes)

        late_minutes = 0
        attendance_status = AttendanceStatus.PRESENT

        if local_now > late_after:
            late_minutes = int((local_now - late_after).total_seconds() // 60)
            attendance_status = AttendanceStatus.LATE

        
        try:
            with transaction.atomic():
                attendance = Attendance.objects.create(
                    employee=employee,
                    date = today_date,
                    check_in=now,
                    late_minutes = late_minutes,
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
                "late_minutes": attendance.late_minutes,
                "status": attendance.status
            }
        }, status=status.HTTP_201_CREATED)
    

class CheckOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        employee = Employee.objects.filter(user=request.user).first()

        if not employee:
            return Response({'message':'Employee profile not found',}, status=status.HTTP_404_NOT_FOUND)

        if employee.employment_status != "ACTIVE":
            return Response({'message':'Your employee account is not active'}, status=status.HTTP_403_FORBIDDEN)

        settings = AttendanceSetting.objects.all().first()
        if not settings:
            return Response({'message':"Attendance settings are not configured"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        today = timezone.localdate()
        attendance = Attendance.objects.filter(employee=employee, date=today).first()

        if not attendance:
            return Response({'message':'You have not checked in today'}, status=status.HTTP_400_BAD_REQUEST)

        if attendance.check_out:
            return Response({'message':'You already have checked out today'}, status=status.HTTP_400_BAD_REQUEST)

        # calculate working duration
        now = timezone.now()
        working_duration = now - attendance.check_in
        required_duration = timedelta(hours=float(settings.required_working_hours))
        half_day_duration =  required_duration / 2

        if working_duration >= half_day_duration:
            working_day_type = WorkingDayType.FUll_DAY
        else:
            working_day_type = WorkingDayType.HALF_DAY


        with transaction.atomic():
            attendance.check_out = now
            attendance.working_duration = working_duration
            attendance.working_day_type = working_day_type

            attendance.save(update_fields=['check_out', 'working_duration', 'working_day_type', 'updated_at'] )

        return Response({
            'message':"Check-out Succesfully",
            "data": {
                "id": attendance.id,
                "date": attendance.date,
                "check_in": attendance.check_in,
                "check_out": attendance.check_out,
                "working_duration": attendance.working_duration,
                "status": attendance.status,
                "working_day_type": attendance.working_day_type
            }
        }, status=status.HTTP_200_OK)


class MyAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employee = Employee.objects.filter(user=request.user).first()

        if not employee:
            return Response(
                {"message": "Employee profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        attendances = Attendance.objects.filter(employee=employee).order_by("-date")

        serializer = MyAttendanceSerializer(attendances, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# Attendance crud
class AttendanceListCreateView(ListCreateAPIView):
    queryset = Attendance.objects.select_related(
        'employee__user',
        'employee__department'
    )
    serializer_class = AttendanceSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ["date", "employee", "status", 'working_day_type']

    search_fields = [
        "employee__user__first_name",
        "employee__user__last_name",
    ]

    ordering_fields = ["date", "check_in", "check_out", "created_at"]
    ordering = ["-date"]

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOrManager]

        return [permission() for permission in permission_classes]
    

class AttendanceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.select_related(
        "employee__user",
        "employee__department"
    )
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOrManager]

        return [permission() for permission in permission_classes]
        



        


        

        
        









        

        
