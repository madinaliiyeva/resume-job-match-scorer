import pathlib
from unittest.mock import MagicMock, patch

import pytest

from src.parser import extract_text


def test_txt_reads_content(tmp_path):
    f = tmp_path / "resume.txt"
    f.write_text("Jane Doe\nPython developer", encoding="utf-8")
    assert extract_text(str(f)) == "Jane Doe\nPython developer"


def test_txt_strips_whitespace(tmp_path):
    f = tmp_path / "resume.txt"
    f.write_text("  \n  some content  \n  ", encoding="utf-8")
    assert extract_text(str(f)) == "some content"


def test_unsupported_extension_raises(tmp_path):
    f = tmp_path / "resume.csv"
    f.write_text("data")
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract_text(str(f))


def test_pdf_extraction(tmp_path):
    fake_page = MagicMock()
    fake_page.extract_text.return_value = "Page one text"

    fake_reader = MagicMock()
    fake_reader.pages = [fake_page]

    # PdfReader is imported lazily inside the function, so patch at source
    with patch("pypdf.PdfReader", return_value=fake_reader):
        f = tmp_path / "resume.pdf"
        f.write_bytes(b"%PDF-1.4 fake")
        result = extract_text(str(f))

    assert result == "Page one text"


def test_pdf_skips_none_pages(tmp_path):
    p1 = MagicMock()
    p1.extract_text.return_value = "First"
    p2 = MagicMock()
    p2.extract_text.return_value = None

    fake_reader = MagicMock()
    fake_reader.pages = [p1, p2]

    with patch("pypdf.PdfReader", return_value=fake_reader):
        f = tmp_path / "resume.pdf"
        f.write_bytes(b"%PDF-1.4 fake")
        result = extract_text(str(f))

    assert result == "First"


def test_docx_extraction(tmp_path):
    p1 = MagicMock()
    p1.text = "Software Engineer"
    p2 = MagicMock()
    p2.text = "5 years Python"

    fake_doc = MagicMock()
    fake_doc.paragraphs = [p1, p2]

    # Document is imported lazily inside the function, so patch at source
    with patch("docx.Document", return_value=fake_doc):
        f = tmp_path / "resume.docx"
        f.write_bytes(b"PK fake docx bytes")
        result = extract_text(str(f))

    assert result == "Software Engineer\n5 years Python"


def test_docx_skips_blank_paragraphs(tmp_path):
    p1 = MagicMock()
    p1.text = "Python"
    p2 = MagicMock()
    p2.text = "   "

    fake_doc = MagicMock()
    fake_doc.paragraphs = [p1, p2]

    with patch("docx.Document", return_value=fake_doc):
        f = tmp_path / "resume.docx"
        f.write_bytes(b"PK fake")
        result = extract_text(str(f))

    assert result == "Python"
