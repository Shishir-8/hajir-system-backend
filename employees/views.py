from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from .serializers import EmployeeSerializer
from .models import Employee
from .permissions import IsAdminOrManager, IsAdminOrManagerOrReadOnly
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class EmployeeBaseView:
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeListView(EmployeeBaseView, ListAPIView):
    permission_classes = [IsAuthenticated]

class EmployeeCreateView(EmployeeBaseView, CreateAPIView):
    permission_classes = [IsAdminOrManager]


class EmployeeDetailView(EmployeeBaseView, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrManagerOrReadOnly]