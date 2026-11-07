from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Employee
from .serializers import EmployeeSerializer

from accounts.permissions import IsAdmin, IsAdminOrManager


# List and Create Employees
class EmployeeListCreateView(ListCreateAPIView):
    queryset = Employee.objects.select_related(
        "user",
        "department",
    )
    serializer_class = EmployeeSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = ["department", "employment_status"]

    search_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
        "designation",
    ]

    ordering_fields = [
        "created_at",
        "joining_date",
        "designation",
    ]

    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOrManager]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return Response(
            {
                "message": "Employee created successfully.",
                "data": response.data,
            },
            status=status.HTTP_201_CREATED,
        )


# Retrieve, Update and Delete Employee
class EmployeeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.select_related(
        "user",
        "department",
    )
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOrManager]

        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        return Response({
            "message": "Employee updated successfully.",
            "data": response.data,
        })

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return Response(
            {"message": "Employee deleted successfully."},
            status=status.HTTP_200_OK,
        )