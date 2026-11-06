from django.urls import path
from .import views



urlpatterns = [
    path('', views.DepartmentListView.as_view()),
    path('create/', views.DepartmentCreateView.as_view()),
    path('<int:pk>/', views.DepartmentDetailView.as_view())
]