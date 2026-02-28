from apps.domain import Family
from apps.infrastructure.external import SqlAlchemyDBClient
from .family_repository import IFamilyRepository
from models import Family as FamilyModel
from .error import NotFoundError


class FamilyRepository(IFamilyRepository):
    def __init__(self, db_client: SqlAlchemyDBClient):
        self._db = db_client

    def add(self, family: Family):
        with self._db.get_transaction_session() as session:
            record = FamilyModel(
                name=family.name,
                nickname=family.nickname,
                gender=family.gender,
                birthday=family.birthday,
                bird_type=family.bird_type,
            )
            session.add(record)
            session.flush()
            return Family(
                name=record.name,
                nickname=record.nickname,
                gender=record.gender,
                birthday=record.birthday,
                bird_type=record.bird_type,
            )

    def get(self, id):
        record = self._db.session.get(FamilyModel, id)
        if record is None:
            raise NotFoundError
        return Family(
            name=record.name,
            nickname=record.nickname,
            gender=record.gender,
            birthday=record.birthday,
            bird_type=record.bird_type,
        )
