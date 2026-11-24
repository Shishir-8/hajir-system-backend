from rest_framework.response import Response
from .models import Leave, LeaveStatus, LeaveType
from .serializers import LeaveSerializer
from rest_framework.views import APIView
from accounts import permissions
from rest_framework.permissions import IsAuthenticated
from employees.models import Employee
from rest_framework import status
from .serializers import LeaveSerializer
from datetime import timedelta

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from attendance.models import Attendance, AttendanceStatus
# Create your views here.


class ApplyLeaveView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        employee = Employee.objects.filter(user=request.user).first()
        if not employee:
            return Response({"message": "Employee Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LeaveSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(employee=employee)
        return Response(
            {
                "message": "Leave request submitted successfully!",
                "results": serializer.data
            },
            status=status.HTTP_200_OK
        )


class MyLeaveListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employee = Employee.objects.filter(user=request.user).first()
        if not employee:
            return Response({"message": "Employee Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        leaves = Leave.objects.filter(employee=employee).select_related("reviewed_by")
        serializer = LeaveSerializer(leaves, many=True)
        return Response(
            {
                "message": "Your leave requests retrieved successfully.",
                "results": serializer.data,
            },
            status=status.HTTP_200_OK
        )



class LeaveListView(APIView):
    permission_classes = [IsAuthenticated, permissions.IsAdminOrManager]

    def get(self, request):
        leaves = Leave.objects.select_related(
            "employee__user",
            "reviewed_by"
        )

        serializer = LeaveSerializer(
            leaves,
            many=True
        )

        return Response(
            {
                "message": "Leave requests retrieved successfully.",
                "results": serializer.data,
            },
            status=status.HTTP_200_OK
        )



class LeaveApprovalView(APIView):
    permission_classes = [IsAuthenticated, permissions.IsAdminOrManager]

    def post(self, request, pk):
        with transaction.atomic():

            leave = get_object_or_404(Leave.objects.select_for_update(),pk=pk)

            if leave.status != LeaveStatus.PENDING:
                return Response({"message": "Only pending leave requests can be approved.",},
                    status=status.HTTP_400_BAD_REQUEST
                )

            current_date = leave.start_date

            while current_date <= leave.end_date:

                attendance = Attendance.objects.filter(
                    employee=leave.employee,
                    date=current_date
                ).first()

                if attendance and attendance.status not in [
                    AttendanceStatus.ABSENT,
                    AttendanceStatus.ON_LEAVE,
                ]:
                    return Response(
                        {
                            "message": (
                                f"Attendance already exists for {current_date}."
                            ),
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                current_date += timedelta(days=1)

            current_date = leave.start_date

            while current_date <= leave.end_date:

                Attendance.objects.update_or_create(
                    employee=leave.employee,
                    date=current_date,
                    defaults={
                        "status": AttendanceStatus.ON_LEAVE
                    }
                )

                current_date += timedelta(days=1)

            leave.status = LeaveStatus.APPROVED
            leave.reviewed_by = request.user
            leave.reviewed_at = timezone.now()

            leave.save(
                update_fields=[
                    "status",
                    "reviewed_by",
                    "reviewed_at",
                ]
            )

        return Response(
            {
                "message": "Leave approved successfully.",
                "results": LeaveSerializer(leave).data,
            },
            status=status.HTTP_200_OK
        )


class LeaveRejectionView(APIView):
    permission_classes = [IsAuthenticated, permissions.IsAdminOrManager]

    def post(self, request, pk):
        leave = get_object_or_404(Leave, pk=pk)

        if leave.status != LeaveStatus.PENDING:
            return Response({
                "message": "Only pending leave requests can be rejected.",
            }, status=status.HTTP_400_BAD_REQUEST)

        leave.status = LeaveStatus.REJECTED
        leave.reviewed_by = request.user
        leave.reviewed_at = timezone.now()

        leave.save(update_fields=[
            "status",
            "reviewed_by",
            "reviewed_at"
        ])

        return Response({
            "success": True,
            "message": "Leave rejected successfully.",
            "results": LeaveSerializer(leave).data
        }, status=status.HTTP_200_OK)


        

class CancelLeaveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        employee = Employee.objects.filter(
            user=request.user
        ).first()

        if not employee:
            return Response({
                "message": "Employee profile not found.",
            }, status=status.HTTP_404_NOT_FOUND)

        leave = get_object_or_404(
            Leave,
            pk=pk,
            employee=employee
        )

        if leave.status != LeaveStatus.PENDING:
            return Response({
                "message": "Only pending leave requests can be cancelled.",
            }, status=status.HTTP_400_BAD_REQUEST)

        leave.status = LeaveStatus.CANCELLED

        leave.save(update_fields=["status", "updated_at"])

        return Response({
            "success": True,
            "message": "Leave request cancelled successfully.",
            "results": LeaveSerializer(leave).data
        }, status=status.HTTP_200_OK)


