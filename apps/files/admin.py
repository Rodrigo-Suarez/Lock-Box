from django.contrib import admin
from .models import File, FileHistory, Folder

# Register your models here.
admin.site.register(Folder)
admin.site.register(File)
admin.site.register(FileHistory)