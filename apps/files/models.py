from django.db import models
from django.contrib.auth.models import User
from google.cloud import storage
from django.conf import settings


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


    def __str__(self):
        return self.name
    

class FileHistory(models.Model):
    file = models.ForeignKey(File, related_name="history", on_delete=models.CASCADE)
    version = models.PositiveIntegerField()
    content = models.CharField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name + self.version
    
