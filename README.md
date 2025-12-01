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

Run the chatbot from the repository root and ask your question in Arabic or
English. Type `quit` or `exit` to leave the session.

```bash
python dreams_chatbot.py
```

This starts an interactive prompt similar to:

```
$ python dreams_chatbot.py
Building index from: /workspace/Tafseer_ahlam/Noor-Book.com  تفسير الاحلام 2  (1).pdf
جاهز للإجابة. اكتب 'quit' أو 'exit' للخروج.

سؤالك: ما تفسير رؤية البحر؟
```

You can also run a single, non-interactive query (helpful if you only want to
grab a quick answer):

```bash
python dreams_chatbot.py --question "ما معنى رؤية البحر في الحلم؟"
```

If the PDF is in a different location, point the script to it with
`--book /path/to/file.pdf`. Use `--top` to adjust how many snippets are
returned and `--chunk-size` to control how the PDF is split for indexing. The
default path is the bundled book at:

```
Noor-Book.com  تفسير الاحلام 2  (1).pdf
```

The bot will search the book for the most relevant passages and return short
excerpts with page numbers.

## Is there a live link to try?

There is no hosted demo at the moment. To try the bot yourself, run the CLI
locally from this repository (or any environment where you place the PDF) and
ask a question directly:

```bash
python dreams_chatbot.py --question "ما معنى رؤية البحر في الحلم؟"
```

If you prefer a chat-style experience, omit `--question` to start the
interactive prompt and type your questions one by one.
