from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"folder", views.FolderViewSet, basename="folder")
router.register(r"file", views.FileViewSet, basename="file")

urlpatterns = [
    path('user/root/', views.RootView.as_view(), name="root"),
    path('file/versions/<int:pk>/', views.FileVersionsView.as_view(), name="versions"),
    path('file/versions/<int:pk>/restore/', views.RestoreFileVersionView.as_view(), name="restore"),
    path('file/history/<int:pk>/', views.FileHistoryView.as_view(), name="file_history"),
    path('folder/history/<int:pk>/', views.FolderHistoryView.as_view(), name="folder_history"),
    path('user/history/', views.HistoryView.as_view(), name="history"),
    path('', include(router.urls)),
]