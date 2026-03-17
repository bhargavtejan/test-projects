#!/usr/bin/env python3
"""CLI tool for converting Word documents to PDF."""

import argparse
import sys
import os
from pathlib import Path
from converter import convert_word_to_pdf


def main():
    parser = argparse.ArgumentParser(
        description="Convert Word documents (.docx/.doc) to PDF",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py document.docx
  python cli.py document.docx -o ./output
  python cli.py *.docx -o ./pdfs
        """,
    )
    parser.add_argument("files", nargs="+", help="Word document(s) to convert (.docx or .doc)")
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output directory for PDF files (default: same directory as input file)",
    )

    args = parser.parse_args()

    success_count = 0
    error_count = 0

    for file_path in args.files:
        input_path = Path(file_path)
        output_dir = args.output if args.output else str(input_path.parent)

        print(f"Converting: {input_path.name} ...", end=" ", flush=True)
        try:
            pdf_path = convert_word_to_pdf(str(input_path), output_dir)
            print(f"Done -> {pdf_path}")
            success_count += 1
        except (FileNotFoundError, ValueError, RuntimeError) as e:
            print(f"FAILED\n  Error: {e}", file=sys.stderr)
            error_count += 1

    print(f"\nCompleted: {success_count} succeeded, {error_count} failed.")
    sys.exit(0 if error_count == 0 else 1)


if __name__ == "__main__":
    main()
