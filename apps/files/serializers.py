from rest_framework import serializers
from .models import Folder, File, FileHistory
from django.contrib.auth.models import User
class FolderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=1)
    author = serializers.CharField(required=True)

    class Meta:
        model = Folder
        fields = ["id", "name", "type", "author", "parent_folder"]


class FileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=1, required=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    content = serializers.CharField(required=True)

    class Meta:
        model = File
        fields = '__all__'
        

class FileHistorySerializer(serializers.ModelSerializer):
    file = serializers.CharField(required=True)

    class Meta:
        model = FileHistory
        fields = ["id", "file", "version", "content"]

