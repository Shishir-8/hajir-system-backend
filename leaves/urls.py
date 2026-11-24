from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.ApplyLeaveView.as_view()),
    path('my-leaves/', views.MyLeaveListView.as_view()),

    path('', views.LeaveListView.as_view()),
    path("approve/<int:pk>/",views.LeaveApprovalView.as_view()),
    path('reject/<int:pk>/', views.LeaveRejectionView.as_view()),
    path('cancel/<int:pk>/', views.CancelLeaveView.as_view())
]