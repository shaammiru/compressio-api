import uuid
from dotenv import dotenv_values
from azure.storage.blob import BlobServiceClient

account_name = dotenv_values()["AZURE_STORAGE_ACCOUNT_NAME"]
account_key = dotenv_values()["AZURE_STORAGE_ACCOUNT_KEY"]
container_name = dotenv_values()["AZURE_STORAGE_CONTAINER_NAME"]
connection_string = dotenv_values()["AZURE_STORAGE_CONNECTION_STRING"]
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)


def upload_blob(folder_name, file_name, data):
    blob_name = f"{folder_name}/{uuid.uuid4()}-{file_name}"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(data)
    return blob_client.url
