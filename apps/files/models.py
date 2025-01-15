from django.db import models
from django.contrib.auth.models import User
from google.cloud import storage
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

class Folder(models.Model):
    name = models.CharField(255, default="new_folder")
    type = models.CharField(255, default="Folder")
    author = models.ForeignKey(User, related_name="folders", on_delete=models.CASCADE)
    parent_folder = models.ForeignKey("self", blank=True, null=True, related_name="sub_folders", on_delete=models.CASCADE) 
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    


class File(models.Model):
    name = models.CharField(255)
    unique_name = models.CharField(255)
    type = models.CharField(255)
    author = models.ForeignKey(User, related_name="files", on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, related_name="files", on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField()
    size = models.PositiveBigIntegerField()
    version = models.PositiveIntegerField(default=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)


    @staticmethod
    def generate_url(unique_filename):
        return f"gs://{settings.GS_BUCKET_NAME}/{unique_filename}"


    @staticmethod
    def generate_unique_name(user_id, filename, replace_existing):
        unique_name = f"{user_id}_{filename}"

        if not replace_existing:
            name, extension = unique_name.split(".")
            counter = 1

            while File.objects.filter(unique_name=unique_name).exists():
                unique_name = f"{name}({counter}){extension}"
                counter += 1

        return unique_name


    def __str__(self):
        return self.name
    

class FileHistory(models.Model):
    file = models.ForeignKey(File, related_name="history", on_delete=models.CASCADE)
    version = models.PositiveIntegerField()
    content = models.CharField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name + self.version
    
