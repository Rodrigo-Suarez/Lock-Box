from rest_framework import serializers
from .models import Folder, File, FileHistory, History
from django.contrib.auth.models import User


class FolderSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=1)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    parent_folder = serializers.PrimaryKeyRelatedField(queryset=Folder.objects.all(), allow_null=True)

    class Meta:
        model = Folder
        fields = '__all__'



class FileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=1, required=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    content = serializers.CharField(required=True)

    class Meta:
        model = File
        fields = '__all__'

        

class FileHistorySerializer(serializers.ModelSerializer):
    file = serializers.PrimaryKeyRelatedField(queryset=File.objects.all(), required=True)
    history_content = serializers.CharField(required=True)
    history_author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)

    class Meta:
        model = FileHistory
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


class FileErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()