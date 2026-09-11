from dataweave.processors.fake_processor import FakeProcessor
from dataweave.processors.registry import ProcessorRegistry


"""
def test_fake_processor_can_process():
    processor = FakeProcessor()

    assert processor.can_process("example.fake")
    assert not processor.can_process("example.pdf")

def test_fake_processor_returns_document():
    processor = FakeProcessor()

    document = processor.process("example.fake")

    assert document.source == "example.fake"
    assert len(document.elements) == 1
    assert document.elements[0].content == "This is a fake document."


def test_registry_retruns_matching_processor():
    registry = ProcessorRegistry()
    fake_processor = FakeProcessor()

    registry.register(fake_processor)

    processor = registry.get_processor("example.fake")

    assert processor is fake_processor


def test_registry_raises_when_no_processor_matches():
    registry = ProcessorRegistry()

    try:
        registry.get_processor("example.pdf")
    except ValueError as er:
        assert str(er) == "No processor found for: example.pdf"

"""