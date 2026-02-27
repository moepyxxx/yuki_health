from abc import ABCMeta, abstractmethod
from typing import BinaryIO
from apps.domain import DailyFamilyFacesImage


class IDailyRecordRepository(metaclass=ABCMeta):
    @abstractmethod
    def upload_feces_image(self, file_obj: BinaryIO, file_name: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def add_faces_image_record(
        self, family_id: str, image_src: str
    ) -> DailyFamilyFacesImage:
        raise NotImplementedError
