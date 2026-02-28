from apps.domain import DailyFamilyFecesImage
from apps.infrastructure.repository import FamilyRepository, DailyRecordRepository
from typing import BinaryIO
from datetime import datetime
from apps.lib.utils import get_extension_from_binary
from apps.infrastructure.repository import NotFoundError
from fastapi import HTTPException
from apps.service.family_faces_analyzer import FamilyFecesAnalyzer


class DailyRecordUseCase:
    def __init__(
        self,
        familyRepository: FamilyRepository,
        dailyRecordRepository: DailyRecordRepository,
        familyFecesAnalyzer: FamilyFecesAnalyzer,
    ):
        self._repository = dailyRecordRepository
        self._familyRepository = familyRepository
        self._familyFecesAnalyzer = familyFecesAnalyzer

    def upload_daily_feces(
        self, family_id: int, file_obj: BinaryIO
    ) -> DailyFamilyFecesImage:
        try:
            self._familyRepository.get(family_id)
        except NotFoundError:
            raise HTTPException(status_code=404)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = get_extension_from_binary(file_obj=file_obj)
        file_name = f"{family_id}/{timestamp}{extension}"

        image_src = self._repository.upload_feces_image(
            file_obj=file_obj, file_name=file_name
        )
        return self._repository.add_daily_feces_image(
            family_id=family_id,
            image_src=image_src,
        )

    def analyze_daily_feces(self, family_id, daily_record_feces_images_id):
        try:
            family = self._familyRepository.get(family_id)
            faces_image_record = self._repository.get_daily_feces_image(
                family_id, daily_record_feces_images_id
            )
        except NotFoundError:
            raise HTTPException(status_code=404)

        if faces_image_record.impressions is not None:
            return

        result = self._familyFecesAnalyzer.invoke(
            image_data=faces_image_record.image_data,
            bird_type=family.bird_type,
            gender=family.gender,
            age_year=family.age_year,
            age_month=family.age_month,
        )

        return self._repository.update_daily_feces_image(
            daily_record_feces_images_id=daily_record_feces_images_id,
            daily_feces_image=DailyFamilyFecesImage(
                image_src=faces_image_record.image_src,
                image_data=faces_image_record.image_data,
                color=result.color,
                has_urates=result.has_urates,
                wateriness=result.wateriness,
                has_undigested_seeds=result.has_undigested_seeds,
                confidence=result.confidence,
                impressions=result.impressions,
            ),
        )
