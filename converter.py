"""Conversion logic for Word <-> PDF using LibreOffice and pdf2docx."""

import subprocess
import shutil
from pathlib import Path


def convert_word_to_pdf(input_path: str, output_dir: str) -> str:
    """Convert a Word document (.docx or .doc) to PDF using LibreOffice."""
    input_path = Path(input_path).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if input_path.suffix.lower() not in (".docx", ".doc"):
        raise ValueError(f"Unsupported file type: {input_path.suffix}. Only .docx and .doc are supported.")

    libreoffice = shutil.which("libreoffice") or shutil.which("soffice")
    if not libreoffice:
        raise RuntimeError("LibreOffice is not installed or not in PATH.")

    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [libreoffice, "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(input_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )

    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion failed:\n{result.stderr}")

    pdf_path = output_dir / (input_path.stem + ".pdf")
    if not pdf_path.exists():
        raise RuntimeError(f"Conversion completed but output PDF not found at: {pdf_path}")

    return str(pdf_path)


def convert_pdf_to_word(input_path: str, output_dir: str) -> str:
    """Convert a PDF file to a Word document (.docx) using pdf2docx."""
    try:
        from pdf2docx import Converter
    except ImportError:
        raise RuntimeError("pdf2docx is not installed. Run: pip install pdf2docx")

    input_path = Path(input_path).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if input_path.suffix.lower() != ".pdf":
        raise ValueError(f"Unsupported file type: {input_path.suffix}. Only .pdf is supported.")

    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    docx_path = output_dir / (input_path.stem + ".docx")

    cv = Converter(str(input_path))
    cv.convert(str(docx_path))
    cv.close()

    if not docx_path.exists():
        raise RuntimeError(f"Conversion completed but output file not found at: {docx_path}")

    return str(docx_path)
