from rest_framework.views import APIView
from .serializers import FolderSerializer, FileSerializer
from .models import Folder, File
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from utils.gcs_service import GCSService
from .utils.unique_filename_generator import unique_filename_generator


class UploadFileView(APIView):
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"detail": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']  #Obtener el archivo de la solicitud

        unique_filename = File.generate_unique_name(request.user.id, file.name, replace_existing=True)
        
        if File.objects.filter(unique_name=unique_filename).exists():
            if not request.data.get("existing", False):
                return Response(
                        {
                            "detail": "File already exists.",
                            "unique_name": unique_filename,
                            "action_required": "confirm",
                            "message": "Do you want to replace the file or save a new version?"
                        },
                        status=status.HTTP_409_CONFLICT
                    )
            
            if not request.data.get("replace_existing", True):
                unique_filename = File.generate_unique_name(request.user.id, file.name, replace_existing=False)

        return self._save_file(request, file, unique_filename)

        

    def _save_file(self, request, file, unique_filename):

        data = {
            "name": file.name,
            "unique_name": unique_filename,
            "type": file.content_type,
            "author": request.user.id,
            #"folder": ,
            "content": File.generate_url(unique_filename),
            "size": file.size,
            #"version": 
        }
        
        serializer = FileSerializer(data=data)
        
        if serializer.is_valid():
            
            try:
                GCSService.upload(unique_filename, file) #Guardar en GCS
                file_instance = serializer.save() #Guardar en la base de datos
                return Response(FileSerializer(file_instance).data, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                GCSService.delete(unique_filename)
                return Response({"detail": "Failed to upload to GCS or save in database", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    






    
 