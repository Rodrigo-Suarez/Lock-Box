from django.conf import settings
from rest_framework.exceptions import ValidationError
from apps.authentication.serializers import ResetPasswordRequestSerializer, ResetPasswordSerializer
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status


class UserService:
    @staticmethod
    def reset_password_request(serializer, backend_url):
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_url = f"{backend_url}/login/reset_password/{user.pk}/{token}"

            send_mail(
                "Restablecer tu contraseña",
                f"Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_url}",
                settings.EMAIL_HOST_USER,
                [email],
            )

            return {"data": "Se ha enviado un enlace para restablecer tu contraseña.", "status": status.HTTP_200_OK}
            
        except User.DoesNotExist:
            return {"data": "El email no está registrado.", "status": status.HTTP_400_BAD_REQUEST}
            
        
    

    @staticmethod
    def reset_password(serializer, user_id):

        new_password = serializer.validated_data['new_password']
        token_from_request = serializer.validated_data['token']
            
        try:
            user = User.objects.get(pk=user_id)
            if not default_token_generator.check_token(user, token_from_request):
                raise ValidationError("El token es inválido o ha expirado.")
                
            user.set_password(new_password)
            user.save()

            return {"data": "Contraseña restablecida con éxito.", "status": status.HTTP_200_OK}
            
        except User.DoesNotExist:
            return {"data": "Usuario no encontrado.", "status": status.HTTP_404_NOT_FOUND}
            
        except ValidationError as e:
            return {"data": str(e), "status": status.HTTP_400_BAD_REQUEST}
            
        

