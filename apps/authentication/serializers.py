from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=5)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("The username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("The username already exists")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
            
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, data):
        user = User.objects.create_user(**data)
        return user
    


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class AuthErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()