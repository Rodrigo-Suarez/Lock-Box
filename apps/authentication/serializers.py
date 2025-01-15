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
        if User.objects.filter(username=value):
            raise serializers.ValidationError("The username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value):
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