from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, ResetPasswordRequestSerializer, ResetPasswordSerializer
from rest_framework.permissions import AllowAny
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from .services.user_service import UserService

class UserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        with transaction.atomic():
            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
            return Response({"detail": "Refresh token was not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class ResetPasswordRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)

        if serializer.is_valid():
            backend_url = f"{request.scheme}://{request.get_host()}"  # Obtiene el dominio del backend
            response = UserService.reset_password_request(serializer, backend_url)

            return Response(response["data"], response["status"])
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk, token):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            response = UserService.reset_password(serializer, pk)

            return Response(response["data"], response["status"])
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)