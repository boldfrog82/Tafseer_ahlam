# Tafseer_ahlam

A simple command-line chatbot that answers questions about dreams using the
included PDF book.

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the chatbot and ask your question in Arabic or English. Type `quit` or
`exit` to leave the session.

```bash
python dreams_chatbot.py
```

You can also run a single, non-interactive query (helpful if you only want to
grab a quick answer):

```bash
python dreams_chatbot.py --question "ما معنى رؤية البحر في الحلم؟"
```

If the PDF is in a different location, point the script to it with
`--book /path/to/file.pdf`. Use `--top` to adjust how many snippets are
returned and `--chunk-size` to control how the PDF is split for indexing.

The bot will search the book for the most relevant passages and return short
excerpts with page numbers.
