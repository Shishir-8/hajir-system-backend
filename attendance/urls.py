from django.urls import path
from . import views


urlpatterns = [
    path('check-in/', views.CheckInView.as_view()),
    path('check-out/', views.CheckOutView.as_view()),
    path('my-attendance/', views.MyAttendanceView.as_view()),

    path('', views.AttendanceListCreateView.as_view()),
    path('<int:pk>/', views.AttendanceDetailView.as_view())

]