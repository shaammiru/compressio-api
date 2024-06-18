import os
import calendar
from datetime import datetime
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"

print(account_name)
print(account_key)
print(container_name)
print(connection_string)

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)


def upload_blob(folder_name, file_name, data):
    unix_time = calendar.timegm(datetime.now().utctimetuple())
    blob_name = f"{folder_name}/{unix_time}-{file_name}"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(data)
    return blob_client.url
