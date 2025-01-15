from google.cloud import storage
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

class GCSService:
    
    @staticmethod
    def upload(unique_filename, file):
        try:
            client = storage.Client(credentials=settings.GS_CREDENTIALS)
            bucket = client.bucket(settings.GS_BUCKET_NAME)
            blob = bucket.blob(unique_filename)
            blob.upload_from_file(file)

        except Exception as e: 
            raise RuntimeError(f"Failed to upload to GCS: {str(e)}")


    @staticmethod
    def delete(unique_filename):
        try:
            client = storage.Client(credentials=settings.GS_CREDENTIALS)
            bucket = client.bucket(settings.GS_BUCKET_NAME)
            blob = bucket.blob(unique_filename)
            blob.delete()  

        except Exception as e:
            raise RuntimeError(f"Failed to upload to GCS: {str(e)}")