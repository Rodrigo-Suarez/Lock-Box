from datetime import datetime, timedelta, timezone
from google.cloud import storage
from django.conf import settings


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
        
    
    @staticmethod
    def rename(old_unique_name, new_unique_name):
        try:
            client = storage.Client(credentials=settings.GS_CREDENTIALS)
            bucket = client.bucket(settings.GS_BUCKET_NAME)
            blob = bucket.blob(old_unique_name)
            
            # Copiar el archivo al nuevo nombre
            bucket.copy_blob(blob, bucket, new_unique_name)
            
            # Eliminar el archivo original
            blob.delete()
        
        except Exception as e:
            raise RuntimeError(f"Failed to upload to GCS: {str(e)}")
        
        
    @staticmethod
    def generate_signed_url(unique_name):
        try:
            client = storage.Client(credentials=settings.GS_CREDENTIALS)
            bucket = client.bucket(settings.GS_BUCKET_NAME)
            blob = bucket.blob(unique_name)
            expiration_time = timedelta(minutes=5)
            url = blob.generate_signed_url(expiration=datetime.now(timezone.utc) + expiration_time, version="v4")
            return url
    
        except Exception as e:
            raise RuntimeError(f"Failed to generate url to GCS: {str(e)}")
        
    @staticmethod
    def duplicate(unique_name, new_unique_name):
        try:
            client = storage.Client(credentials=settings.GS_CREDENTIALS)
            bucket = client.bucket(settings.GS_BUCKET_NAME)
            blob = bucket.blob(unique_name)
            bucket.copy_blob(blob, bucket, new_unique_name)

        except Exception as e:
            raise RuntimeError(f"Failed to duplicate to GCS: {str(e)}")