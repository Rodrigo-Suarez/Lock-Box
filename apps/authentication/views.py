from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

class UserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        with transaction.atomic():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                return Response(UserSerializer(user).data)
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