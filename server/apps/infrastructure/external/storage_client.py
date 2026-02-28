import boto3
from typing import BinaryIO
from botocore.exceptions import ClientError
import base64


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
        self._resource = boto3.resource(
            "s3",
            endpoint_url=endpoint_base_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_password,
            region_name=region,
        )

    def upload_file(self, bucket_name: str, file_obj: BinaryIO, file_name: str):
        bucket = self._resource.Bucket(bucket_name)
        try:
            bucket.upload_fileobj(file_obj, file_name)
        except Exception as e:
            raise StorageClientError(f"Failed to add object: {e}")

    def get_file_data_from_object_key(self, bucket_name: str, object_key: str) -> str:
        try:
            print(object_key)
            res = self._resource.Object(bucket_name, object_key).get()
        except ClientError as e:
            raise e
        image_bytes: bytes = res["Body"].read()
        b64: bytes = base64.b64encode(image_bytes).decode()
        return f"data:image/png;base64,{b64}"

    def get_object_key_from_image_src(self, bucket_name: str, image_src: str) -> str:
        return image_src.removeprefix(f"{bucket_name}/")
