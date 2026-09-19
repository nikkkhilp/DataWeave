import pytest
from dataweave.core.exceptions import (
    DataWeaveError,
    ProcessingError,
)


def test_processing_error_is_dataweave_error():
    error = ProcessingError("PDF processing failed")

    assert isinstance(error, DataWeaveError)
    assert str(error) == "PDF processing failed"