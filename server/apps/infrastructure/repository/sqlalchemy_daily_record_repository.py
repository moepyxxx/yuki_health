from .daily_record_repository import IDailyRecordRepository
from apps.infrastructure.external import SqlAlchemyDBClient
from apps.infrastructure.external import StorageClient
from typing import BinaryIO
from apps.domain import DailyFamilyFacesImage
from models import DailyFamilyFacesImage as DailyFamilyFacesImageModel

DAILY_FAMILY_FACES_BUCKET_NAME = "daily-family-feces"


class DailyRecordRepository(IDailyRecordRepository):
    def __init__(self, db_client: SqlAlchemyDBClient, storage_client: StorageClient):
        self._db_client = db_client
        self._storage_client = storage_client

    def upload_feces_image(self, file_obj: BinaryIO, file_name: str) -> str:
        self._storage_client.upload_file(
            DAILY_FAMILY_FACES_BUCKET_NAME, file_obj=file_obj, file_name=file_name
        )
        return f"{DAILY_FAMILY_FACES_BUCKET_NAME}/{file_name}"

    def add_faces_image_record(self, family_id, file_name) -> DailyFamilyFacesImage:
        image_src = f"{DAILY_FAMILY_FACES_BUCKET_NAME}/{file_name}"
        with self._db.get_session() as session:
            record = DailyFamilyFacesImageModel(
                family_id=family_id,
                image_src=image_src,
            )
            session.add(record)
            session.flush()
            return DailyFamilyFacesImage(name=record.name, image_path=record.image_path)


# TODO: モデル見直し。file_name, file_path など混在。パスだけ保存すればOK
