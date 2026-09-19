from dataweave.core.pipeline import ProcessingStage

def test_processing_stage_can_be_implemented():
    class TestStage(ProcessingStage):
        def run(self, document):
            return document

    stage = TestStage()

    assert stage is not None