from dataweave.core.raw import (
    RawSpan,
    RawLine,
    RawBlock,
    RawPage,
)


def test_raw_span():
    span = RawSpan(
        text="Hello",
        font="Arial",
        size=12.0,
        flags=0,
        bbox=(10.0, 20.0, 50.0, 35.0),
    )

    assert span.text == "Hello"
    assert span.font == "Arial"
    assert span.size == 12.0
    assert span.bbox == (10.0, 20.0, 50.0, 35.0)


def test_raw_line_contains_spans():
    span = RawSpan(text="Hello")

    line = RawLine(
        line_num=1,
        spans=[span],
    )

    assert line.line_num == 1
    assert line.spans[0].text == "Hello"


def test_raw_block_contains_lines():
    line = RawLine(line_num=1)

    block = RawBlock(
        block_num=1,
        block_type=0,
        lines=[line],
    )

    assert block.block_num == 1
    assert block.lines[0].line_num == 1


def test_raw_page_contains_blocks():
    block = RawBlock(block_num=1)

    page = RawPage(
        page_num=1,
        width=595.0,
        height=842.0,
        blocks=[block],
    )

    assert page.page_num == 1
    assert page.width == 595.0
    assert page.blocks[0].block_num == 1