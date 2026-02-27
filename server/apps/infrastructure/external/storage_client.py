import boto3
from typing import BinaryIO


class StorageClientError(Exception):
    """StorageClientError"""


class StorageClient:
    def __init__(
        self,
        endpoint_base_url: str,
        access_key_id: str,
        access_key_password: str,
        region: str,
    ):
        self.client = boto3.resource(
            "s3",
            endpoint_url=endpoint_base_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_password,
            region_name=region,
        )

    def upload_file(self, bucket_name: str, file_obj: BinaryIO, file_name: str):
        bucket = self.client.Bucket(bucket_name)
        try:
            bucket.upload_fileobj(file_obj, file_name)
        except Exception as e:
            raise StorageClientError(f"Failed to add object: {e}")
