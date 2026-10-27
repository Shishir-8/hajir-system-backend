from django.urls import path
from . import views


urlpatterns = [
    path('', views.EmployeeListView.as_view()),
    path('create/', views.EmployeeCreateView.as_view()),
    path('<int:pk>/', views.EmployeeDetailView.as_view())
]