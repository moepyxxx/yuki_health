from abc import ABCMeta, abstractmethod
from typing import Any


class VectorDBClient(metaclass=ABCMeta):
    @abstractmethod
    def add(
        self,
        collection_name: str,
        document: str,
        id: str,
        metadata: Any,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def query(
        self,
        collection_name: str,
        query: str,
        n_results: int = 5,
    ) -> Any:
        raise NotImplementedError
