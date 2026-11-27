from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import Department
from .serializers import DepartmentSerializer
from accounts.permissions import IsAdmin, IsAdminOrManager
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend


class DepartmentListCreateView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    filter_backends =[SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ["is_active"]
    
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