"""Core Word to PDF conversion logic using LibreOffice."""

import subprocess
import shutil
import os
from pathlib import Path


def convert_word_to_pdf(input_path: str, output_dir: str) -> str:
    """
    Convert a Word document (.docx or .doc) to PDF using LibreOffice.

    Args:
        input_path: Path to the input Word document.
        output_dir: Directory where the PDF will be saved.

    Returns:
        Path to the generated PDF file.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the file is not a Word document.
        RuntimeError: If conversion fails.
    """
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
