import pathlib


def extract_text(file_path: str) -> str:
    """Extract plain text from a PDF or DOCX resume file."""
    path = pathlib.Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return _extract_from_pdf(path)
    elif suffix in (".docx", ".doc"):
        return _extract_from_docx(path)
    elif suffix == ".txt":
        return path.read_text(encoding="utf-8").strip()
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Expected .pdf, .docx, or .txt")


def _extract_from_pdf(path: pathlib.Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def _extract_from_docx(path: pathlib.Path) -> str:
    from docx import Document

    doc = Document(str(path))
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(paragraphs).strip()
