from dataweave.core.models import CanonicalDocument
from abc import ABC, abstractmethod

class DocumentProcessor(ABC):
    @abstractmethod
    def can_process(self, file_path:str) -> bool:
        pass

    @abstractmethod
    def process(self, file_path:str) -> CanonicalDocument:
        pass