#!/usr/bin/env python3
"""CLI tool for converting Word <-> PDF."""

import argparse
import sys
from pathlib import Path
from converter import convert_word_to_pdf, convert_pdf_to_word


def main():
    parser = argparse.ArgumentParser(
        description="Convert between Word (.docx/.doc) and PDF — direction is auto-detected from the file extension",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py document.docx          # Word -> PDF
  python cli.py report.pdf             # PDF  -> Word
  python cli.py document.docx -o ./out
  python cli.py *.pdf -o ./word_files
        """,
    )
    parser.add_argument("files", nargs="+", help="File(s) to convert (.docx, .doc, or .pdf)")
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output directory (default: same directory as input file)",
    )

    args = parser.parse_args()

    success_count = 0
    error_count = 0

    for file_path in args.files:
        input_path = Path(file_path)
        output_dir = args.output if args.output else str(input_path.parent)
        suffix = input_path.suffix.lower()

        print(f"Converting: {input_path.name} ...", end=" ", flush=True)
        try:
            if suffix in (".docx", ".doc"):
                result = convert_word_to_pdf(str(input_path), output_dir)
            elif suffix == ".pdf":
                result = convert_pdf_to_word(str(input_path), output_dir)
            else:
                raise ValueError(f"Unsupported file type: {suffix}. Use .docx, .doc, or .pdf.")
            print(f"Done -> {result}")
            success_count += 1
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            print(f"FAILED\n  Error: {e}", file=sys.stderr)
            error_count += 1

    print(f"\nCompleted: {success_count} succeeded, {error_count} failed.")
    sys.exit(0 if error_count == 0 else 1)


if __name__ == "__main__":
    main()
