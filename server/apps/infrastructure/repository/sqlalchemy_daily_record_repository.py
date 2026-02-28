from .daily_record_repository import IDailyRecordRepository
from apps.infrastructure.external import SqlAlchemyDBClient
from apps.infrastructure.external import StorageClient
from typing import BinaryIO
from apps.domain import DailyFamilyFecesImage
from models import DailyFamilyFecesImage as DailyFamilyFecesImageModel
from .error import NotFoundError, DataIntegrityError

DAILY_FAMILY_FECES_BUCKET_NAME = "daily-family-feces"


class DailyRecordRepository(IDailyRecordRepository):
    def __init__(self, db_client: SqlAlchemyDBClient, storage_client: StorageClient):
        self._db_client = db_client
        self._storage_client = storage_client

    def upload_feces_image(self, file_obj: BinaryIO, file_name: str) -> str:
        self._storage_client.upload_file(
            DAILY_FAMILY_FECES_BUCKET_NAME, file_obj=file_obj, file_name=file_name
        )
        return f"{DAILY_FAMILY_FECES_BUCKET_NAME}/{file_name}"

    def add_daily_feces_image(self, family_id, image_src) -> DailyFamilyFecesImage:
        with self._db_client.get_transaction_session() as session:
            record = DailyFamilyFecesImageModel(
                family_id=family_id,
                image_src=image_src,
            )
            session.add(record)
            session.flush()
            image_data = self._get_image_data(record.image_src)
            return DailyFamilyFecesImage(image_src=image_src, image_data=image_data)

    def get_daily_feces_image(
        self, family_id: int, daily_record_feces_images_id: int
    ) -> DailyFamilyFecesImage:
        record = self._db_client.session.get(
            DailyFamilyFecesImageModel, daily_record_feces_images_id
        )
        if record is None or record.family_id != family_id:
            raise NotFoundError
        image_data = self._get_image_data(record.image_src)
        return DailyFamilyFecesImage(
            image_src=record.image_src,
            image_data=image_data,
            color=record.color,
            has_urates=record.has_urates,
            wateriness=record.wateriness,
            has_undigested_seeds=record.has_undigested_seeds,
            confidence=record.confidence,
            impressions=record.impressions,
        )

    def update_daily_feces_image(
        self,
        daily_record_feces_images_id: int,
        daily_feces_image: DailyFamilyFecesImage,
    ) -> DailyFamilyFecesImage:
        with self._db_client.get_transaction_session() as session:
            record = session.get(
                DailyFamilyFecesImageModel, daily_record_feces_images_id
            )
            if record is None:
                raise NotFoundError
            if record.image_src != daily_feces_image.image_src:
                raise DataIntegrityError("image_src column is cannot update")
            record.color = daily_feces_image.color
            record.has_urates = daily_feces_image.has_urates
            record.wateriness = daily_feces_image.wateriness
            record.has_undigested_seeds = daily_feces_image.has_undigested_seeds
            record.confidence = daily_feces_image.confidence
            record.impressions = daily_feces_image.impressions
            session.flush()
            image_data = self._get_image_data(record.image_src)

            return DailyFamilyFecesImage(
                image_src=record.image_src,
                image_data=image_data,
                color=record.color,
                has_urates=record.has_urates,
                wateriness=record.wateriness,
                has_undigested_seeds=record.has_undigested_seeds,
                confidence=record.confidence,
                impressions=record.impressions,
            )

    def _get_image_data(self, image_src: str) -> str:
        return self._storage_client.get_file_data_from_object_key(
            bucket_name=DAILY_FAMILY_FECES_BUCKET_NAME,
            object_key=self._storage_client.get_object_key_from_image_src(
                bucket_name=DAILY_FAMILY_FECES_BUCKET_NAME, image_src=image_src
            ),
        )
