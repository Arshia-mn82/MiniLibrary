# src/storage.py
import json
from pathlib import Path
from typing import List
from .models import Book

DATA_PATH = Path("data/books.json")

def ensure_data_file() -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_PATH.exists():
        DATA_PATH.write_text("[]", encoding="utf-8")

def load_books() -> List[Book]:
    ensure_data_file()
    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return [Book.from_dict(x) for x in raw]

def save_books(books: List[Book]) -> None:
    ensure_data_file()
    raw = [b.to_dict() for b in books]
    DATA_PATH.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

def next_id(books: List[Book]) -> int:
    return (max((b.id for b in books), default=0) + 1)
