from abc import ABCMeta, abstractmethod
from typing import BinaryIO
from apps.domain import DailyFamilyFecesImage


class IDailyRecordRepository(metaclass=ABCMeta):
    @abstractmethod
    def upload_feces_image(self, file_obj: BinaryIO, file_name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def add_daily_feces_image(
        self, family_id: int, image_src: str
    ) -> DailyFamilyFecesImage:
        raise NotImplementedError

    @abstractmethod
    def update_daily_feces_image(
        self, family_id: int, daily_feces_image: DailyFamilyFecesImage
    ) -> DailyFamilyFecesImage:
        raise NotImplementedError

    @abstractmethod
    def get_daily_feces_image(
        self, family_id: int, daily_record_feces_images_id: int
    ) -> DailyFamilyFecesImage:
        raise NotImplementedError
