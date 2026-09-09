from dataweave.processors.base import DocumentProcessor

class ProcessorRegistry:
    def __init__(self):
        self._processors : list[DocumentProcessor] = []

    def register(self, processor: DocumentProcessor) -> None:
        self._processors.append(processor)

    def get_processor(self, file_path: str) -> DocumentProcessor:
        for processor in self._processors:
            if processor.can_process(file_path):
                return processor
        raise ValueError(f"No processor found for: {file_path}")
