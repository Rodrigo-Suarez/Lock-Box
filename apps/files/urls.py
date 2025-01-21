from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"folder", views.FolderViewSet, basename="folder")
router.register(r"file", views.FileViewSet, basename="file")

urlpatterns = [
    path('root/', views.RootView.as_view(), name="root"),
    path('', include(router.urls)),
]