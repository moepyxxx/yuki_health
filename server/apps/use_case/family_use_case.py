from apps.domain import Family
from apps.infrastructure.repository import FamilyRepository


class FamilyUseCase:
    def __init__(
        self,
        familyRepository: FamilyRepository,
    ):
        self._repository = familyRepository

    def create(self, family: Family):
        return self._repository.add(family=family)
