from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .services.file_service import FileService
from .services.folder_service import FolderService
from .models import File, Folder
from .serializers import FileSerializer, FolderSerializer



class RootView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            folders = FolderService.get_root_folders(request.user.id)
            files = FileService.get_root_files(request.user.id)
            return Response(folders["data"] + files["data"], status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": "Error al obtener archivos y carpetas", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES['file'] 

        if not file:
            return Response({"detail": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        response = FileService.process_upload(
            user_id = request.user.id,
            file = file,
            existing = request.data.get("existing", False),
            replace_existing = request.data.get("replace_existing", True),
            folder = request.data.get("folder", None)
        )

        return Response(response["data"], response["status"])


    @action(methods=["patch"], detail=True, url_name="rename")
    def rename(self, request, pk):
        response = FileService.rename(
            file_id = pk,
            user_id = request.user.id,
            new_name = request.data.get("name")
        )

        return Response(response["data"], response["status"])
    

    @action(methods=["patch"], detail=True, url_name="relocate")
    def relocate(self, request, pk):
        response = FileService.relocate(
            file_id = pk,
            user_id = request.user.id,
            new_folder = request.data.get("folder")
        )

        return Response(response["data"], response["status"])

        

class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer


    def create(self, request, *args, **kwargs):  
        response = FolderService.create_folder(
            name = request.data.get("name", "new_folder"),
            user_id = request.user.id,
            parent_folder = request.data.get("parent_folder", None)
        )
        
        return Response(response["data"], response["status"])
    
    
    def retrieve(self, request, *args, **kwargs):
        response = FolderService.get_folder(
            folder_id = kwargs.get("pk"),
            user_id = request.user.id
        )

        return Response(response["data"], response["status"])
    
        