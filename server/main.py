from fastapi import FastAPI, UploadFile, Path, File, Body
from dotenv import load_dotenv

from apps.domain import Family, DailyFamilyFacesImage
from apps.use_case import FamilyUseCase, DailyRecordUseCase
from apps.infrastructure.external import SqlAlchemyDBClient
from apps.infrastructure.repository import FamilyRepository, DailyRecordRepository
from apps.infrastructure.external import StorageClient

import os

load_dotenv()
app = FastAPI()

database_url = os.getenv("POSTGRES_DATABASE_URL")
storage_endpoint_url = os.getenv("STORAGE_ENDPOINT_URL")
storage_access_key_id = os.getenv("STORAGE_ACCESS_KEY_ID")
storage_access_key_password = os.getenv("STORAGE_ACCESS_KEY_PASSWORD")

family_use_case = FamilyUseCase(
    FamilyRepository(db_client=SqlAlchemyDBClient(database_url))
)
daily_report_use_case = DailyRecordUseCase(
    FamilyRepository(db_client=SqlAlchemyDBClient(database_url)),
    DailyRecordRepository(
        db_client=SqlAlchemyDBClient(database_url),
        storage_client=StorageClient(
            endpoint_base_url=storage_endpoint_url,
            access_key_id=storage_access_key_id,
            access_key_password=storage_access_key_password,
            region="ap-northeast-1",
        ),
    ),
)


@app.post("/families", response_model=Family)
def create_family(family: Family = Body()):
    family = family_use_case.create(family=family)
    return family


@app.post(
    "/families/{family_id}/daily_record/feces", response_model=DailyFamilyFacesImage
)
def upload_daily_family_faces_image(
    family_id: int = Path(...), file: UploadFile = File(...)
):
    return daily_report_use_case.upload_daily_feces(
        family_id=family_id, file_obj=file.file
    )
