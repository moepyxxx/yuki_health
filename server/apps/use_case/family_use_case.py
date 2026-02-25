from apps.domain import Family
from apps.infrastructure.repository import FamilyRepository


class FamilyUseCase:
    def __init__(self, familyRepository: FamilyRepository):
        self.repository = familyRepository

    def create(self, family: Family):
        return self.repository.add(family=family)
