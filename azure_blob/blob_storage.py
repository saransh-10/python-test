from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

class AzureBlobStorage:
    def __init__(self):
        """
        Initialize the AzureBlobStorage class with connection details.
        """
        self.connection_string = "DefaultEndpointsProtocol=https;AccountName=stmlhayyadevwe001;AccountKey=GAkXvvk5zIR5K1cowlUbG7W/P/J2NOHP06wngkev/BxOzqV/JcKdeIjkwh+WyPHOUdCU1kV1onpz+AStL6d9KQ==;EndpointSuffix=core.windows.net"
        self.container_name = "bot-graphs"
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)


    def upload_image(self, file_path, blob_name):
        """
        Upload an image to Azure Blob Storage.
        :param file_path: Path to the image file to upload.
        :param blob_name: Name of the blob in Azure Blob Storage.
        """
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f"Uploaded {file_path} as {blob_name}")
        except Exception as e:
            print(f"Error uploading image: {e}")

    def download_image(self, blob_name, download_path):
        """
        Download an image from Azure Blob Storage.
        :param blob_name: Name of the blob to download.
        :param download_path: Path to save the downloaded image.
        """
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            with open(download_path, "wb") as data:
                data.write(blob_client.download_blob().readall())
            print(f"Downloaded {blob_name} to {download_path}")
        except Exception as e:
            print(f"Error downloading image: {e}")

    def list_blobs(self):
        """
        List all blobs in the container.
        :return: List of blob names.
        """
        try:
            blob_list = [blob.name for blob in self.container_client.list_blobs()]
            print("Blobs in container:")
            for blob in blob_list:
                print(f" - {blob}")
            return blob_list
        except Exception as e:
            print(f"Error listing blobs: {e}")
            return []
