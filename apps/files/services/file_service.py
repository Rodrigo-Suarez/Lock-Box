from apps.files.models import File, Folder
from apps.files.utils.data import generate_history_data, generate_file_data
from apps.files.serializers import FileHistorySerializer, FileSerializer
from apps.files.models import FileHistory, File
from rest_framework import status
from services.gcs_service import GCSService
from django.db import transaction



class FileService():
    @staticmethod
    def process_upload(user_id, file, existing, replace_existing, folder):
        unique_filename = File.generate_unique_name(user_id, file.name, folder, replace_existing=True)
        file_db = File.objects.filter(unique_name=unique_filename).first()
        
        if file_db:
            if not existing:
                return {
                    "data":{
                        "detail": "File already exists.",
                        "unique_name": unique_filename,
                        "action_required": "confirm",
                        "message": "Do you want to replace the file or save a new version?"
                        },
                        
                    "status": status.HTTP_409_CONFLICT
                }
            
            if replace_existing:
                return FileService._replace_file(user_id, file_db, file, folder)

            unique_filename = File.generate_unique_name(user_id, file.name, folder, replace_existing)
                
        return FileService._new_file(user_id, file, unique_filename, folder)



    @staticmethod
    def _new_file(user_id, file, unique_filename, folder):
        data = generate_file_data(file, user_id, unique_filename, folder)
        serializer = FileSerializer(data=data)

        if serializer.is_valid():
            try:
                GCSService.upload(unique_filename, file) #Guardar en GCS
                file_instance = serializer.save() #Guardar en la base de datos
                return {"data": FileSerializer(file_instance).data, "status": status.HTTP_201_CREATED}
            
            except Exception as e:
                GCSService.delete(unique_filename)
                raise RuntimeError({"detail": "Failed to upload to GCS or save in database", "error": str(e)})

        return {"data": serializer.errors, "status":status.HTTP_400_BAD_REQUEST}


    @staticmethod
    def _replace_file(user_id, file_db, file, folder):
        unique_filename = FileHistory.generate_unique_name(user_id, file.name, file_db.version, folder)
        data = generate_history_data(file_db, unique_filename, user_id)
        serializer = FileHistorySerializer(data=data)

        if serializer.is_valid():
            try:
                GCSService.rename(file_db.unique_name, unique_filename)
                GCSService.upload(file_db.unique_name, file) #Guardar en GCS
                with transaction.atomic():
                    file_db.version += 1
                    file_db.save()
                    file_instance = serializer.save() #Guardar en la base de datos
                    return {"data": FileHistorySerializer(file_instance).data, "status": status.HTTP_201_CREATED}
            
            except Exception as e:
                GCSService.delete(unique_filename)
                raise RuntimeError({"detail": "Failed to upload to GCS or save in database", "error": str(e)})

        return {"data": serializer.errors, "status":status.HTTP_400_BAD_REQUEST}
    

    @staticmethod
    def get_root_files(user_id):
        try:
            files = File.objects.filter(author=user_id, folder=None)
            serializer = FileSerializer(files, many=True)
            return {"data": serializer.data}
        
        except Exception as e:
            raise RuntimeError({"detail":"file error" ,"error": str(e)})
        
    
    @staticmethod
    def rename(file_id, user_id, new_name):
        file = File.objects.filter(id=file_id, author=user_id).first()

        if file:
            if file.name == new_name or not new_name:
                return {"data": "choose another name", "status":status.HTTP_400_BAD_REQUEST}
            
            with transaction.atomic():
                try:
                    new_unique_name = File.generate_unique_name(user_id, new_name, file.folder.id, replace_existing=True)
                    GCSService.rename(file.unique_name, new_unique_name)
                    file.name = new_name
                    file.unique_name = new_unique_name
                    file.content = File.generate_url(new_unique_name)
                    file.save()
                    serializer = FileSerializer(file)
                    return {"data": serializer.data, "status": status.HTTP_201_CREATED}

                except Exception as e:
                    GCSService.rename(new_unique_name, file.unique_name)
                    raise RuntimeError({"detail":"file error" ,"error": str(e)})
                
        return {"data": "file not found", "status":status.HTTP_404_NOT_FOUND}
    

    @staticmethod
    def relocate(file_id, user_id, new_folder):
        file = File.objects.filter(id=file_id, author=user_id).first()
        if file:
            folder = Folder.objects.filter(id=new_folder, author=user_id).first()

            if file.folder == folder:
                return {"data": "choose another folder", "status":status.HTTP_400_BAD_REQUEST}

            with transaction.atomic():
                try:
                    new_unique_name = File.generate_unique_name(user_id, file.name, new_folder, replace_existing=True)
                    GCSService.rename(file.unique_name, new_unique_name)
                    file.folder = folder
                    file.unique_name = new_unique_name
                    file.content = File.generate_url(new_unique_name)
                    file.save()
                    serializer = FileSerializer(file)
                    return {"data": serializer.data, "status": status.HTTP_201_CREATED}
                
                except Exception as e:
                    GCSService.rename(new_unique_name, file.unique_name)
                    raise RuntimeError({"detail":"file error" ,"error": str(e)})

        return {"data": "file not found", "status":status.HTTP_404_NOT_FOUND}