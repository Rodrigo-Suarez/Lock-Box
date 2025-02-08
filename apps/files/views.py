from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from .services.file_service import FileService
from .services.folder_service import FolderService
from .services.file_history_service import FileHistoryService
from .services.history_service import HistoryService
from .models import File, Folder
from .serializers import FileHistorySerializer, FileSerializer, FolderSerializer, FileErrorSerializer, HistorySerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.parsers import MultiPartParser, FormParser
from .utils.params import get_change, get_existing, get_new_folder, get_replace_existing, get_folder



class RootView(APIView):
    @extend_schema(
        summary="Root folder",
        description="Endpoint to navigate to the user's root folder.",
        responses={
            200: OpenApiResponse(description='Successful response with the content of the root folder'),
            500: FileErrorSerializer,
        }
    )
    
    def get(self, request):
        try:
            folders = FolderService.get_root_folders(request.user.id)
            files = FileService.get_root_files(request.user.id)
            return Response(folders["data"] + files["data"], status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": "Error al obtener archivos y carpetas", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FileViewSet(
    mixins.RetrieveModelMixin,   # Permite GET /files/{id}/
    mixins.CreateModelMixin,     # Permite POST /files/
    mixins.DestroyModelMixin,    # Permite DELETE /files/{id}/
    viewsets.GenericViewSet      # No incluye list
):
    
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        summary="Upload file",
        description="Endpoint to upload a file.",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "existing": {"type": "boolean"},
                    "replace_existing": {"type": "boolean"},
                    "file": {
                        "type": "string",
                        "format": "binary"  # Esto indica que es un archivo
                    },
                    "folder": {"type": "integer"},
                }
            }
        },
        responses={
            200: FileSerializer,
            400: FileErrorSerializer,
            500: FileErrorSerializer,
        }
    )
    def create(self, request):
        if 'file' not in request.FILES:
            return Response({"detail": "No file was uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file'] 
        try:
            existing = get_existing(request.data.get("existing"))
            replace_existing = get_replace_existing(request.data.get("replace_existing"))
            folder = get_folder(request.data.get("folder"))

        except (ValueError, TypeError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response = FileService.process_upload(
            user_id = request.user.id,
            file = file,
            existing = existing,
            replace_existing = replace_existing,
            folder = folder
        )

        return Response(response["data"], response["status"])
    

    @extend_schema(
        summary="Get file",
        description="Endpoint to get a signed URL to download a file.",
        responses={
            200: FileSerializer,
            500: FileErrorSerializer,
        }
    )
    def retrieve(self, request, pk):
        
        response = FileService.get_signed_url(pk, request.user.id)
        return Response(response["data"], response["status"])

    @extend_schema(
        summary="update file",
        description="Endpoint to change the name/folder of a file.",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "folder": {"type": "integer"},
                    "change": {"type": "boolean"}
                }
            }
        },
        responses={
            201: FileSerializer,
            500: FileErrorSerializer,
        }
    )
    def partial_update(self, request, pk):
        try:
            new_name = request.data.get("name")
            new_folder = get_new_folder(request.data.get("folder"))
            change = get_change(request.data.get("change"))

        except (ValueError, TypeError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response = []

        if new_name:
            updated_file_name = FileService.rename(pk, request.user.id, new_name, change)
            response.append(updated_file_name["data"])

        if new_folder:
            updated_file_folder = FileService.relocate(pk, request.user.id, new_folder, change)
            response.append(updated_file_folder["data"])

        return Response(response, status.HTTP_201_CREATED)
    

    
    def destroy(self, request, pk):
        file = get_object_or_404(File, id=pk, author=request.user.id)
        self.perform_destroy(file)

        return Response(status=status.HTTP_204_NO_CONTENT)
    


class FolderViewSet(
    mixins.RetrieveModelMixin,   # Permite GET /files/{id}/
    mixins.CreateModelMixin,     # Permite POST /files/
    mixins.DestroyModelMixin,    # Permite DELETE /files/{id}/
    viewsets.GenericViewSet      # No incluye list
):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    parser_classes = [MultiPartParser, FormParser] 

    @extend_schema(
        summary="Create folder",
        description="Endpoint to create a new folder.",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "parent_folder": {"type": "integer"},
                    "change": {"type": "boolean"}
                }
            }
        },
        responses={
            200: FolderSerializer,
            500: FileErrorSerializer,
        }
    )

    def create(self, request):  
        try:
            parent_folder = get_folder(request.data.get("parent_folder"))
            change = get_change(request.data.get("change"))

        except (ValueError, TypeError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        response = FolderService.create_folder(
            name = request.data.get("name", "new_folder"),
            user_id = request.user.id,
            parent_folder = parent_folder,
            change = change
        )
        
        return Response(response["data"], response["status"])
    
    @extend_schema(
        summary="Get folder",
        description="Endpoint to get a folder with its content.",
        responses={
            200: FolderSerializer,
            500: FileErrorSerializer,
        }
    )  
    def retrieve(self, request, pk):
        response = FolderService.get_folder(pk, request.user.id)
        return Response(response["data"], response["status"])
    

    @extend_schema(
        summary="update file",
        description="Endpoint to change the name/folder of a file.",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "parent": {"type": "integer"},
                    "change": {"type": "boolean"}
                }
            }
        },
        responses={
            201: FolderSerializer,
            500: FileErrorSerializer,
        }
    )
    def partial_update(self, request, pk):
        try:
            new_name = request.data.get("name")
            new_parent = get_new_folder(request.data.get("parent"))
            change = get_change(request.data.get("change"))

        except (ValueError, TypeError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response = []

        if new_name:
            updated_folder_name = FolderService.rename(pk, request.user.id, new_name, change)
            response.append(updated_folder_name["data"])

        if new_parent:
            updated_folder_parent = FolderService.relocate(pk, request.user.id, new_parent, change)
            response.append(updated_folder_parent["data"])

        return Response(response, status.HTTP_201_CREATED)
    


    def destroy(self, request, pk):
        folder = get_object_or_404(Folder, id=pk, author=request.user.id)
        self.perform_destroy(folder)

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class FileVersionsView(APIView):
    @extend_schema(
        summary="Get file versions",
        description="Endpoint to get the history of versions of a file.",
        responses={
            200: FileHistorySerializer,
            500: FileErrorSerializer,
        }
    )
    def get(self, request, pk):
        response = FileHistoryService.get_versions(pk, request.user.id) 
        return Response(response["data"], response["status"])


class RestoreFileVersionView(APIView):
    @extend_schema(
        summary="Restore file version",
        description="Endpoint to restore a version of a file.",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "version_id": {"type": "integer"}
                }
            }
        },
        responses={
            200: FileHistorySerializer,
            500: FileErrorSerializer,
        }
    )
    def post(self, request, pk):
        try:
            version_id = int(request.data.get("version_id"))
        except (ValueError, TypeError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        response = FileHistoryService.restore_version(
            file_id = pk,
            user_id = request.user.id,
            version_id = version_id
        )

        return Response(response["data"], response["status"])
    

class HistoryView(APIView):
    @extend_schema(
        summary="Get user history",
        description="Endpoint to get the history of actions of a user.",
        responses={
            200: HistorySerializer,
            500: FileErrorSerializer,
        }
    )
    def get(self, request):
        response = HistoryService.get_user_history(request.user.id)
        return Response(response["data"], response["status"])
    

class FileHistoryView(APIView):
    @extend_schema(
        summary="Get file history",
        description="Endpoint to get the history of actions of a file.",
        responses={
            200: HistorySerializer,
            500: FileErrorSerializer,
        }
    )
    def get(self, request, pk):
        response = HistoryService.get_file_history(pk, request.user.id)
        return Response(response["data"], response["status"])


class FolderHistoryView(APIView):
    @extend_schema(
        summary="Get folder history",
        description="Endpoint to get the history of actions of a folder.",
        responses={
            200: HistorySerializer,
            500: FileErrorSerializer,
        }
    )
    def get(self, request, pk):
        response = HistoryService.get_folder_history(pk, request.user.id)
        return Response(response["data"], response["status"])