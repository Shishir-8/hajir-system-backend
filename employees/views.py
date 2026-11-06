from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import EmployeeSerializer
from .models import Employee
from accounts.permissions import IsAdmin, IsAdminOrManager
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
# Create your views here.

class EmployeeListView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminOrManager]

    filter_backends= [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields  = ["department"]
    search_fields = ['user__first_name', "user__last_name"]
    ordering_fields = ["created_at", 'joining_date']


class EmployeeCreateView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdmin]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message':"Employee created succesfully",
            "data": response.data
        }, status=status.HTTP_201_CREATED)


class EmployeeDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAdminOrManager]
        return [permission() for permission in permission_classes]
    

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'message':"Employee Update Succesfully",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            'message':"Employee deleted succesfully"
        }, status=status.HTTP_204_NO_CONTENT)
        


    