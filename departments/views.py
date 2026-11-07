from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import Department
from .serializers import DepartmentSerializer
from accounts.permissions import IsAdmin, IsAdminOrManager


class DepartmentListCreateView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOrManager]

        return [permission() for permission in permission_classes]
    

class DepartmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'PATCH']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOrManager]

        return [permission() for permission in permission_classes]