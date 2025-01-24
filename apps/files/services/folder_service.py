from apps.files.models import Folder, File
from apps.files.serializers import FolderSerializer, FileSerializer
from apps.files.utils.data import generate_folder_data
from rest_framework import status
from django.db import transaction
from rest_framework.exceptions import ValidationError


class FolderService():

    @staticmethod
    def create_folder(name, user_id, parent_folder, change):
        name = FolderService.process_patch(name, user_id, parent_folder, change)
        data = generate_folder_data(name, user_id, parent_folder)
        serializer = FolderSerializer(data=data)

        if serializer.is_valid():
            folder_instance = serializer.save()
            return {"data": FolderSerializer(folder_instance).data, "status": status.HTTP_201_CREATED}
        
        return {"data": serializer.errors, "status":status.HTTP_400_BAD_REQUEST}
    


    @staticmethod
    def get_root_folders(user_id):
        try:
            folders = Folder.objects.filter(author=user_id, parent_folder=None)
            serializer = FolderSerializer(folders, many=True)
            return {"data": serializer.data}
        
        except Exception as e:
            raise RuntimeError({"detail":"folder error" ,"error": str(e)})
        
    

    @staticmethod
    def get_folder(folder_id, user_id):
        try:
            folders = Folder.objects.filter(parent_folder=folder_id, author=user_id)
            files = File.objects.filter(folder=folder_id, author=user_id)
            folders_serializer = FolderSerializer(folders, many=True)
            files_serializer = FileSerializer(files, many=True)
            return {"data": folders_serializer.data + files_serializer.data, "status": status.HTTP_200_OK}

        except Exception as e:
            raise RuntimeError({"detail":"folder error" ,"error": str(e)})
        


    @staticmethod
    def process_patch(name, user_id, folder_id, change):
        folder_db = Folder.objects.filter(name=name, author=user_id, parent_folder=folder_id).first()
        new_unique_name = Folder.generate_name(name, user_id, folder_id)

        if folder_db and change == False:
            raise ValidationError({
                    "data":{
                        "detail": "Folder already exists.",
                        "unique_name": folder_db.name,
                        "action_required": "confirm",
                        "message": f"Do you want to cancel the operation or save the file as: {new_unique_name}?"
                        }
                })
        
        return new_unique_name



    @staticmethod
    def rename(folder_id, user_id, new_name, change):
        folder = Folder.objects.filter(id=folder_id, author=user_id).first()

        if folder:
            if folder.name == new_name:
                return {"data": "choose another name"}
            
            if not folder.parent_folder:
                folder_id = None
            else:
                folder_id = folder.parent_folder.id
            
            new_folder_name = FolderService.process_patch(new_name, user_id, folder_id, change)
            
            with transaction.atomic():
                try:
                    folder.name = new_folder_name
                    folder.save()
                    serializer = FolderSerializer(folder)
                    return {"data": serializer.data}

                except Exception as e:
                    raise RuntimeError({"detail":"folder error" ,"error": str(e)})


        return {"data": "folder not found"}







