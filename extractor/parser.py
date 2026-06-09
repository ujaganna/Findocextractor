import io
import pdfplumber
from bs4 import BeautifulSoup


def parse_pdf(file_bytes: bytes) -> str:
    """Extract all text from a PDF SEC filing, page by page."""
    text_pages = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_pages.append(text)
    return "\n".join(text_pages)


def parse_html(file_bytes: bytes) -> str:
    """Strip HTML tags from an SEC filing and return clean plain text."""
    soup = BeautifulSoup(file_bytes, "lxml")
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


def parse_filing(file_bytes: bytes, filename: str) -> str:
    """Route to PDF or HTML parser based on file extension."""
    if filename.lower().endswith(".pdf"):
        return parse_pdf(file_bytes)
    return parse_html(file_bytes)
