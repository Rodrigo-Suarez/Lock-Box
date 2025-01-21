from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from services.gcs_service import GCSService


class Folder(models.Model):
    name = models.CharField(255, default="new_folder")
    author = models.ForeignKey(User, related_name="folders", on_delete=models.CASCADE)
    parent_folder = models.ForeignKey("self", null=True, related_name="sub_folders", on_delete=models.CASCADE) 
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)


    def delete(self, *args, **kwargs):
        for file in self.files.all():
            GCSService.delete(file.unique_name)
            file.delete()

        super().delete(*args, **kwargs)


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


    def delete(self, *args, **kwargs):
        GCSService.delete(self.unique_name)

        for history in self.history.all():
            GCSService.delete(history.history_unique_name)

        super().delete(*args, **kwargs)


    @staticmethod
    def generate_url(unique_filename):
        return f"gs://{settings.GS_BUCKET_NAME}/{unique_filename}"


    @staticmethod
    def generate_unique_name(user_id, filename, folder, replace_existing):
        unique_name = f"{user_id}_{folder}_{filename}"

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
    history_author = models.ForeignKey(User, related_name="history", on_delete=models.CASCADE)
    history_unique_name = models.CharField(255)
    history_version = models.PositiveIntegerField()
    history_content = models.CharField()
    history_size = models.PositiveBigIntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    
    
    @staticmethod
    def generate_unique_name(user_id, filename, version, folder):
        unique_name = f"{user_id}_V{version}_{folder}_{filename}"
        return unique_name

    def __str__(self):
        return f"{self.file.name} V{self.history_version}"
    
