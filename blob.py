import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, AccountSasPermissions

def upload_image_to_container(container_name,image_name,filepath):
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container = ContainerClient.from_connection_string(connect_str, container_name)
    try:
        container_properties = container.get_container_properties()
    except Exception as e:
        container_client = blob_service_client.create_container(container_name)
        print("container now created!")
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=image_name)
    print("\nUploading to Azure Storage as blob:\n\t" + image_name)
    with open(filepath, "rb") as data:
        blob_client.upload_blob(data)
    print("data uploaded")