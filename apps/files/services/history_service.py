from apps.files.models import History, File, Folder
from apps.files.serializers import HistorySerializer
from rest_framework import status

class HistoryService:
    @staticmethod
    def get_user_history(user_id):
        history = History.objects.filter(author=user_id).all()
        if history:
            try:
                serializer = HistorySerializer(history, many=True)
                return {"data": serializer.data, "status": status.HTTP_200_OK}
            
            except Exception as e:
                raise RuntimeError({"detail":"Something went wrong" ,"error": str(e)})
            
        return {"data": "Still no changes"}
    

    @staticmethod
    def get_file_history(file_id, user_id):
        file = File.objects.filter(id=file_id, author=user_id).first()

        if file:    
            history = file.actions.all()
            if history:
                try:
                    serializer = HistorySerializer(history, many=True)
                    return {"data": serializer.data, "status": status.HTTP_200_OK}
                
                except Exception as e:
                    raise RuntimeError({"detail":"Something went wrong" ,"error": str(e)})
                
            return {"data": "Still no changes", "status": status.HTTP_404_NOT_FOUND}
        
        return {"data": "file not found", "status": status.HTTP_404_NOT_FOUND}
    

    @staticmethod
    def get_folder_history(folder_id, user_id):
        folder = Folder.objects.filter(id=folder_id, author=user_id).first()

        if folder:
            history = folder.actions.all()
            if history:
                try:
                    serializer = HistorySerializer(history, many=True)
                    return {"data": serializer.data, "status": status.HTTP_200_OK}
                
                except Exception as e:
                    raise RuntimeError({"detail":"Something went wrong" ,"error": str(e)})
                
            return {"data": "Still no changes", "status": status.HTTP_404_NOT_FOUND}
        
        return {"data": "folder not found", "status": status.HTTP_404_NOT_FOUND}
        