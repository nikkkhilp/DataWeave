class DataWeaveError(Exception):
    """Base exception for DataWeave."""


class ProcessingError(DataWeaveError): 
    """Raised when document processing fails."""