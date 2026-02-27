from apps.domain import DailyFamilyFacesImage
from apps.infrastructure.repository import FamilyRepository, DailyRecordRepository
from typing import BinaryIO
from datetime import date
from server.apps.lib.utils import get_extension_from_binary
from apps.infrastructure.repository import NotFoundError
from fastapi import HttpException


class DailyRecordUseCase:
    def __init__(
        self,
        familyRepository: FamilyRepository,
        dailyRecordRepository: DailyRecordRepository,
    ):
        self.repository = dailyRecordRepository
        self.familyRepository = familyRepository

    def upload_daily_feces(
        self, family_id: int, file_obj: BinaryIO
    ) -> DailyFamilyFacesImage:
        try:
            self.familyRepository.get(family_id)
        except NotFoundError as e:
            raise HttpException(status_code=404)

        timestamp = date.now().strftime("%Y%m%d")
        extension = get_extension_from_binary(file_obj=file_obj)
        file_name = f"{family_id}/{timestamp}{extension}"

        image_src = self.repository.upload_feces_image(
            file_obj=file_obj, file_name=file_name
        )
        return self.repository.add_faces_image_record(
            family_id=family_id,
            file_name=image_src,
        )
