from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

    path('forgot-password/', views.PasswordResetRequestView.as_view()),
    path('change-password/', views.ChangePasswordView.as_view()),

]