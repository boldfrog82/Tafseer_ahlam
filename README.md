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

The bot will search the book for the most relevant passages and return short
excerpts with page numbers.
