from apps.files.models import FileHistory, File
from apps.files.serializers import FileHistorySerializer
from rest_framework import status
from apps.files.utils.data import generate_history_data
from services.gcs_service import GCSService
from django.db import transaction
from apps.files.signals import restored_file


class FileHistoryService:
    @staticmethod
    def get_versions(file_id, user_id):
        file = File.objects.filter(id=file_id, author=user_id).first()
        if file:
            history = file.history.all()
            serializer = FileHistorySerializer(history, many=True)
            return {"data": serializer.data, "status": status.HTTP_200_OK}

        return {"data": "File not found", "status": status.HTTP_404_NOT_FOUND}
    

    @staticmethod
    def restore_version(file_id, user_id, version_id):
        file = File.objects.filter(id=int(file_id), author=user_id).first()
        if file:
            old_version = FileHistory.objects.filter(id=int(version_id), file=file.id, history_author=user_id).first()
            if old_version:
                unique_filename = FileHistory.generate_unique_name(user_id, file.name, file.version, file.folder)
                data = generate_history_data(file, unique_filename, user_id)
                serializer = FileHistorySerializer(data=data)
                if serializer.is_valid():
                    try:
                        GCSService.rename(file.unique_name, unique_filename)
                        GCSService.duplicate(old_version.history_unique_name, file.unique_name)
                        with transaction.atomic():
                            file.size = old_version.history_size
                            file.version += 1
                            file._restoring = True
                            restored_file.send(sender=File, instance=file, old_version=old_version.history_version)
                            file.save()
                            file._restoring = False
                            file_instance = serializer.save() #Guardar en la base de datos
                            return {"data": FileHistorySerializer(file_instance).data, "status": status.HTTP_201_CREATED}
                        
                    except Exception as e:
                        GCSService.delete(unique_filename)
                        raise RuntimeError({"detail": "Failed to upload to GCS or save in database", "error": str(e)})

                return {"data": serializer.errors, "status":status.HTTP_400_BAD_REQUEST}

            return {"data": "Version not found", "status": status.HTTP_404_NOT_FOUND}

        return {"data": "File not found", "status": status.HTTP_404_NOT_FOUND}
