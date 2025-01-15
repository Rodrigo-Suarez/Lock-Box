from rest_framework.views import APIView
from .serializers import FolderSerializer, FileSerializer
from .models import Folder, File
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from utils.gcs_service import GCSService
import .utils import 


class UploadFileView(APIView):
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"detail": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']  #Obtener el archivo de la solicitud
        unique_filename =
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
    


    






    
 