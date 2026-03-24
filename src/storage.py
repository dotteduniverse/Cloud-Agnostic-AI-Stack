from abc import ABC, abstractmethod
import os
from src.config import config

class BaseStorage(ABC):
    @abstractmethod
    def upload_file(self, local_path: str, remote_key: str):
        pass

    @abstractmethod
    def download_file(self, remote_key: str, local_path: str):
        pass

    @abstractmethod
    def list_files(self, prefix: str = ""):
        pass

class S3Storage(BaseStorage):
    def __init__(self, bucket_name):
        import boto3
        self.s3 = boto3.client("s3")
        self.bucket = bucket_name

    def upload_file(self, local_path: str, remote_key: str):
        self.s3.upload_file(local_path, self.bucket, remote_key)

    def download_file(self, remote_key: str, local_path: str):
        self.s3.download_file(self.bucket, remote_key, local_path)

    def list_files(self, prefix: str = ""):
        resp = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        return [obj["Key"] for obj in resp.get("Contents", [])]

class AzureStorage(BaseStorage):
    def __init__(self, connection_string, container_name):
        from azure.storage.blob import BlobServiceClient
        self.client = BlobServiceClient.from_connection_string(connection_string)
        self.container = container_name

    def upload_file(self, local_path: str, remote_key: str):
        blob_client = self.client.get_blob_client(container=self.container, blob=remote_key)
        with open(local_path, "rb") as f:
            blob_client.upload_blob(f, overwrite=True)

    def download_file(self, remote_key: str, local_path: str):
        blob_client = self.client.get_blob_client(container=self.container, blob=remote_key)
        with open(local_path, "wb") as f:
            data = blob_client.download_blob().readall()
            f.write(data)

    def list_files(self, prefix: str = ""):
        container_client = self.client.get_container_client(self.container)
        blobs = container_client.list_blobs(name_starts_with=prefix)
        return [blob.name for blob in blobs]

def get_storage_client():
    cloud = config["cloud"]
    storage_cfg = config["storage"]
    if cloud == "aws":
        bucket = storage_cfg["bucket_name"]
        return S3Storage(bucket)
    elif cloud == "azure":
        conn_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
        container = storage_cfg["container_name"]
        return AzureStorage(conn_str, container)
    else:
        raise ValueError(f"Unsupported cloud: {cloud}")