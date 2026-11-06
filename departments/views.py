from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Department
from .serializers import DepartmentSerializer

from accounts.permissions import IsAdmin, IsAdminOrManager


class DepartmentListView(ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminOrManager]


class DepartmentCreateView(CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdmin]


class DepartmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [IsAdminOrManager]
        else:
            permission_classes = [IsAdmin]

        return [permission() for permission in permission_classes]