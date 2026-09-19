from abc import ABC, abstractmethod
from dataweave.core.models import CanonicalDocument

class ProcessingStage(ABC):

    @abstractmethod
    def run(self, document: CanonicalDocument) -> CanonicalDocument:
        pass