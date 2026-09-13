from dataclasses import dataclass, field, asdict
import json


@dataclass
class Element:
    element_id: str
    type: str
    content: str
    page: int
    raw: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    source: dict = field(default_factory=dict)

@dataclass
class CanonicalDocument:
    document_id: str
    source: str
    metadata: dict = field(default_factory=dict)
    elements: list[Element] = field(default_factory=list)

    def to_dict(self) -> dict :
        return asdict(self)

@dataclass
class TextSpan:
    text: str
    font: str | None = None
    size: float | None = None
    flags: int = 0
    bbox: tuple[float, float, float, float] | None = None

@dataclass
class NormalizedLine:
    bbox : tuple[float, float, float, float] | None = None
    spans: list[TextSpan] = field(default_factory=list)

@dataclass
class NormalizedBlock:
    block_type: int
    bbox      : tuple[float, float, float, float] | None = None
    lines     : list[NormalizedLine] = field(default_factory=list)

"""
So the hierarchy becomes: 
                        NormalizedBlock
                            │
                            └── NormalizedLine
                                    │
                                    └── TextSpan
"""

@dataclass
class LineFeatures:
    text      : str
    bbox      : tuple[float, float, float, float] | None=None

    font_sizes: list[float]  =field(default_factory=list) 
    fonts     : list[str]    =field(default_factory=list)
    flags     : list[int]    =field(default_factory=list)

    text_length : int=0
    is_bold     : bool=False
    is_italic   : bool=False

    #positional features
    x_pos        : float | None = None
    y_pos        : float | None = None
    space_before : float | None = None
    space_after  : float | None = None
    indentation  : float | None = None

@dataclass
class LineClassification:
    type       : str
    confidence : float
    reasons    : list[str] = field(default_factory=list)

@dataclass
class ClassifiedLine:
    features       : LineFeatures
    classification : LineClassification

@dataclass
class SemanticElement:
    type       : str
    content    : str
    page       : int
    lines      : list[ClassifiedLine] = field(default_factory=list)
    confidence : float = 0.0


@dataclass
class VisualLineGroup:
    lines : list[NormalizedLine] = field(default_factory=list)
    bbox  : tuple[float,float,float,float] | None=None