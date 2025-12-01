"""
Simple command-line chatbot that answers dream interpretation questions using
content from the included PDF book.

The bot indexes the PDF into TF–IDF vectors and returns the most relevant
paragraphs for a user question. This keeps the responses grounded in the
source material without requiring external services.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence
import argparse
import re
import sys

from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BOOK_PATH = Path("Noor-Book.com  تفسير الاحلام 2  (1).pdf")


@dataclass
class TextChunk:
    """A piece of text tied to its page number."""

    page: int
    content: str

    def short_excerpt(self, length: int = 350) -> str:
        """Return a trimmed excerpt for display purposes."""
        excerpt = self.content.strip()
        if len(excerpt) <= length:
            return excerpt
        return excerpt[: length - 1].rsplit(" ", 1)[0] + "…"


class DreamInterpreter:
    """Indexes and queries the dream interpretation book."""

    def __init__(self, book_path: Path = BOOK_PATH, *, chunk_size: int = 900) -> None:
        self.book_path = book_path
        self.chunk_size = chunk_size
        self.vectorizer: TfidfVectorizer | None = None
        self.matrix = None
        self.chunks: List[TextChunk] = []

    def load(self) -> None:
        """Read the PDF and build a TF–IDF index for similarity search."""
        self.chunks = list(self._pdf_chunks(self.book_path, chunk_size=self.chunk_size))
        corpus = [chunk.content for chunk in self.chunks]
        # Use character n-grams for better coverage of Arabic without relying on tokenization.
        self.vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(3, 5), min_df=2)
        self.matrix = self.vectorizer.fit_transform(corpus)

    def answer(self, question: str, *, top_n: int = 3) -> str:
        """Return book-grounded text snippets that relate to the question."""
        if not question.strip():
            return "Please provide a question about your dream."

        if self.vectorizer is None or self.matrix is None:
            raise RuntimeError("Interpreter has not been loaded. Call load() first.")

        query_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(query_vector, self.matrix)[0]
        ranked_indices = scores.argsort()[::-1][:top_n]

        responses = []
        for idx in ranked_indices:
            score = scores[idx]
            if score <= 0:
                continue
            chunk = self.chunks[idx]
            responses.append(
                f"• (Page {chunk.page}) {chunk.short_excerpt()}"
            )

        if not responses:
            return (
                "لم أجد مقطعًا مرتبطًا بسؤالك مباشرة. حاول استخدام كلمات مفتاحية "
                "أكثر تحديدًا من النص أو رموز الرؤيا."
            )

        intro = (
            "فيما يلي أقرب المقاطع من كتاب تفسير الأحلام ذات الصلة بسؤالك. "
            "استخدمها كمرجع ولا تعتبرها فتوى قاطعة:")
        return "\n".join([intro, *responses])

    @staticmethod
    def _pdf_chunks(path: Path, *, chunk_size: int) -> Iterable[TextChunk]:
        """Yield text chunks from each page, splitting on paragraphs and length."""
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")

        reader = PdfReader(str(path))
        for page_idx, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = DreamInterpreter._normalize_whitespace(text)
            for paragraph in text.split("\n"):
                normalized = paragraph.strip()
                if not normalized:
                    continue
                for chunk in DreamInterpreter._split_text(normalized, chunk_size):
                    yield TextChunk(page=page_idx, content=chunk)

    @staticmethod
    def _split_text(text: str, chunk_size: int) -> Sequence[str]:
        """Split long text into manageable chunks without cutting words."""
        if len(text) <= chunk_size:
            return [text]

        parts: List[str] = []
        start = 0
        while start < len(text):
            end = min(len(text), start + chunk_size)
            # Try to break on a space going backwards for readability.
            space = text.rfind(" ", start, end)
            if space == -1 or space <= start:
                space = end
            parts.append(text[start:space].strip())
            start = space
        return [p for p in parts if p]

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Answer dream questions using the bundled Tafseer Ahlam PDF. "
            "Run interactively with no arguments or pass a single question "
            "via --question."
        )
    )
    parser.add_argument(
        "-q",
        "--question",
        help="Ask one question non-interactively and print the answer.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=3,
        help="Number of snippets to return for each question (default: 3).",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=900,
        help="Characters per chunk when indexing the PDF (default: 900).",
    )
    parser.add_argument(
        "--book",
        type=Path,
        default=BOOK_PATH,
        help="Path to the Tafseer Ahlam PDF (default: bundled file).",
    )
    return parser


def _run_cli(argv: Sequence[str] | None = None) -> None:
    parser = _build_arg_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    interpreter = DreamInterpreter(book_path=args.book, chunk_size=args.chunk_size)
    print("Building index from the dream interpretation book...", file=sys.stderr)
    interpreter.load()

    if args.question:
        print(interpreter.answer(args.question, top_n=args.top))
        return

    print("جاهز للإجابة. اكتب 'quit' أو 'exit' للخروج.\n")

    while True:
        try:
            question = input("سؤالك: ").strip()
        except EOFError:
            print()  # newline for clean exit
            break

        if question.lower() in {"quit", "exit"}:
            break

        answer = interpreter.answer(question, top_n=args.top)
        print(f"\n{answer}\n")


if __name__ == "__main__":
    _run_cli()
