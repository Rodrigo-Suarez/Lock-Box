from apps.files.models import Folder, File
from apps.files.serializers import FolderSerializer, FileSerializer
from apps.files.utils.data import generate_folder_data
from rest_framework import status

class FolderService():

    @staticmethod
    def create_folder(name, user_id, parent_folder):
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


