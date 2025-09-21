# Tafseer_ahlam

This repository contains the Tafseer Ahlam source PDF along with tooling to convert it into UTF-8 encoded text suitable for downstream processing.

## Requirements

* Python 3.10+
* [pdfminer.six](https://github.com/pdfminer/pdfminer.six) for PDF text extraction

Install the dependency with:

```bash
pip install pdfminer.six
```

## Extracting the text corpus

Run the extraction script to regenerate the normalized text file:

```bash
python scripts/extract_text.py --input "Noor-Book.com  تفسير الاحلام 2  (1).pdf" --output data/tafseer_ahlam.txt
```

The script normalizes Unicode output, trims repetitive headers/footers, and preserves paragraph boundaries before writing to `data/tafseer_ahlam.txt` using UTF-8 encoding.
