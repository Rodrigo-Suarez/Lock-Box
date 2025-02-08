from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('auth/register/', views.UserView.as_view(), name="register"),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/reset_password/', views.ResetPasswordRequestView.as_view(), name='password_reset_request'),
    path('auth/login/reset_password/<int:pk>/<str:token>/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
