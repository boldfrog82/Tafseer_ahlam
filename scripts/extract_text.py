#!/usr/bin/env python3
"""Extract and normalize Arabic text from the Tafseer Ahlam PDF."""

from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path

from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams


def _default_input_path() -> Path:
    return Path(__file__).resolve().parent.parent / "Noor-Book.com  تفسير الاحلام 2  (1).pdf"


def _default_output_path() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "tafseer_ahlam.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract normalized Arabic text from the Tafseer Ahlam PDF."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=_default_input_path(),
        help="Path to the input PDF file. Defaults to the repository PDF.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=_default_output_path(),
        help="Path to the output text file. Defaults to data/tafseer_ahlam.txt.",
    )
    return parser.parse_args()


HEADER_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"^Noor-Book",
        r"^www\.",
        r"تفسير الأحلام",
        r"^\d+\s*/\s*\d+$",
    ]
]


def normalize_line(line: str) -> str:
    line = unicodedata.normalize("NFKC", line)
    line = line.replace("\ufeff", "")
    return line.strip()


def should_drop_line(line: str) -> bool:
    if not line:
        return False
    if line.isdigit():
        return True
    return any(pattern.search(line) for pattern in HEADER_PATTERNS)


def normalize_text(raw_text: str) -> str:
    lines = [normalize_line(line) for line in raw_text.splitlines()]
    filtered_lines = []
    for line in lines:
        if should_drop_line(line):
            continue
        filtered_lines.append(line)

    normalized_paragraphs = []
    blank_run = 0
    for line in filtered_lines:
        if not line:
            blank_run += 1
        else:
            if blank_run > 0 and (not normalized_paragraphs or normalized_paragraphs[-1] != ""):
                normalized_paragraphs.append("")
            blank_run = 0
            normalized_paragraphs.append(line)
    normalized_text = "\n".join(normalized_paragraphs).strip()
    if normalized_text:
        normalized_text += "\n"
    return normalized_text


def extract_pdf_text(pdf_path: Path) -> str:
    laparams = LAParams()
    return extract_text(pdf_path, laparams=laparams)


def main() -> None:
    args = parse_args()
    pdf_path: Path = args.input
    output_path: Path = args.output

    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    raw_text = extract_pdf_text(pdf_path)
    normalized_text = normalize_text(raw_text)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(normalized_text, encoding="utf-8")

    print(f"Extracted text saved to {output_path}")


if __name__ == "__main__":
    main()
