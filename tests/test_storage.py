import pytest
from unittest.mock import MagicMock, patch
from src.storage import S3Storage, AzureStorage

def test_s3_upload():
    mock_s3 = MagicMock()
    with patch("boto3.client", return_value=mock_s3):
        s3 = S3Storage("my-bucket")
        s3.upload_file("local.txt", "remote.txt")
        mock_s3.upload_file.assert_called_once_with("local.txt", "my-bucket", "remote.txt")

def test_azure_upload():
    mock_blob = MagicMock()
    with patch("azure.storage.blob.BlobServiceClient.from_connection_string") as mock_client:
        mock_client.return_value.get_blob_client.return_value.upload_blob = mock_blob
        az = AzureStorage("conn_str", "container")
        az.upload_file("local.txt", "remote.txt")
        mock_blob.assert_called_once()