from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LogoutSerializer, AuthErrorSerializer
from rest_framework.permissions import AllowAny
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from .services.user_service import UserService
from drf_spectacular.utils import extend_schema


class UserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    @extend_schema(
        auth=[],
        summary="Register a new user",
        description="Endpoint to register a new user.",
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: AuthErrorSerializer
        }
    )

    def post(self, request):
        with transaction.atomic():
            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    @extend_schema(
        summary="logout",
        description="Endpoint to logout a user.",
        request={
            "application/json": {
                "example": {
                    "refresh_token": "my_secure_token_12345"
                }
            }
        },
        responses={
            205: {"description": "Logout successful."},
            400: {"description": "Error"},
        }
    )
    
    def post(self, request):
        try:
            serializer = LogoutSerializer(data=request.data)

            if serializer.is_valid():
                refresh_token = serializer.validated_data["refresh_token"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class ResetPasswordRequestView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        operation_id="password_reset_request",
        auth=[],
        summary="Reset password request",
        description="Endpoint to request a password change using email.",
        request={
            "application/json": {
                "example": {
                    "email": "user@email.com"
                }
            }
        },
        responses={
            200: {"description": "Se ha enviado un enlace para restablecer tu contraseña."},
            400: {"description": "El email no está registrado."},
        }
    )

    def post(self, request):
        backend_url = f"{request.scheme}://{request.get_host()}"  # Obtiene el dominio del backend
        response = UserService.reset_password_request(request.data.get("email"), backend_url)

        return Response(response["data"], response["status"])
        


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="password_reset",
        auth=[],
        summary="Reset password",
        description="Endpoint to change the password.",
        request={
            "application/json": {
                "example": {
                    "new_password": "abcd1234"
                }
            }
        },
        responses={
            201: {"description": "password restored successfuly."},
            404: {"description": "User not found."},
            400: {"description": "Bad request"}
        }
    )

    def post(self, request, pk, token):
        response = UserService.reset_password(request.data.get("new_password"), pk, token)

        return Response(response["data"], response["status"])
    