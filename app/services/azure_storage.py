from azure.storage.blob import BlobServiceClient
from flask import current_app
import os

class AzureStorageService:
    def __init__(self):
        connection_string = current_app.config['AZURE_STORAGE_CONNECTION_STRING']
        if not connection_string:
            raise ValueError("Azure Storage connection string not configured")
            
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = current_app.config['AZURE_CONTAINER_NAME']
        
    def upload_file(self, file_path, blob_name):
        """Upload a file to Azure Blob Storage."""
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
                
            return blob_client.url
            
        except Exception as e:
            current_app.logger.error(f"Azure upload error: {str(e)}")
            raise
            
    def delete_file(self, blob_name):
        """Delete a file from Azure Blob Storage."""
        try:
            blob_client = self.blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            blob_client.delete_blob()
            
        except Exception as e:
            current_app.logger.error(f"Azure delete error: {str(e)}")
            raise 