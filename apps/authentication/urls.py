from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('register/', views.UserView.as_view(), name="register"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/reset_password/', views.ResetPasswordRequestView.as_view(), name='password_reset_request'),
    path('login/reset_password/<int:pk>/<str:token>/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
