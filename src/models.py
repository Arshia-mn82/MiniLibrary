# src/models.py
from dataclasses import dataclass, asdict

@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Book":
        return Book(
            id=int(d["id"]),
            title=str(d["title"]),
            author=str(d["author"]),
            year=int(d["year"]),
        )
