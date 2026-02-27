from abc import ABCMeta, abstractmethod
from apps.domain import Family


class IFamilyRepository(metaclass=ABCMeta):
    @abstractmethod
    def add(self, family: Family) -> Family:
        raise NotImplementedError

    @abstractmethod
    def get(self, id: int) -> Family:
        raise NotImplementedError
