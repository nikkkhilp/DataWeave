from dataclasses import dataclass, field 

@dataclass
class RawSpan:
    text: str
    font: str   | None=None
    size: float | None=None
    flags: int  | None=None
    bbox: tuple[float, float, float, float] | None=None

@dataclass
class RawLine:
    line_num: int
    bbox: tuple[float, float, float, float] | None=None
    spans: list[RawSpan] = field(default_factory=list)

@dataclass
class RawBlock:
    block_num: int
    block_type: int | None=None
    bbox: tuple[float, float, float, float] | None=None
    lines: list[RawLine] = field(default_factory=list)

@dataclass
class RawPage:
    page_num: int
    width: float
    height: float
    rotation: int=0
    blocks: list[RawBlock] = field(default_factory=list)


@dataclass
class RawEvidence:
    parser: str
    pages: list[RawPage] = field(default_factory=list)