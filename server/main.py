from fastapi import FastAPI
from dotenv import load_dotenv

from apps.domain import Family
from apps.use_case import FamilyUseCase
from apps.infrastructure.external import SqlAlchemyDBClient
from apps.infrastructure.repository import FamilyRepository

import os

load_dotenv()
app = FastAPI()

database_url = os.getenv("POSTGRES_DATABASE_URL")
family_use_case = FamilyUseCase(
    FamilyRepository(db_client=SqlAlchemyDBClient(database_url))
)


@app.post("/families", response_model=Family)
def create_family(family: Family):
    family = family_use_case.create(family=family)
    return family
