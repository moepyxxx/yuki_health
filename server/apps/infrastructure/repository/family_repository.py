from abc import ABCMeta, abstractmethod
from apps.domain import Family


class IFamilyRepository(metaclass=ABCMeta):
    @abstractmethod
    def add(self, family: Family) -> Family:
        raise NotImplementedError
