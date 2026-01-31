# src/app.py
from __future__ import annotations

from .models import Book
from .storage import load_books, save_books, next_id


def _fmt_book_line(book: Book) -> str:
    return f"[{book.id}] {book.title} | {book.author} | {book.year}"


def _print_book(book: Book) -> None:
    print(_fmt_book_line(book))


def show_all(books: list[Book]) -> None:
    if not books:
        print("Library is empty.")
        return
    for item in books:
        _print_book(item)


def create_book() -> None:
    catalog = load_books()

    raw_title = input("Book title: ").strip()
    raw_author = input("Author name: ").strip()
    raw_year = input("Published year: ").strip()

    if not raw_title:
        print("Error: title is required.")
        return
    if not raw_author:
        print("Error: author is required.")
        return
    if not raw_year.isdigit():
        print("Error: year must be numeric.")
        return

    entry = Book(
        id=next_id(catalog),
        title=raw_title,
        author=raw_author,
        year=int(raw_year),
    )
    catalog.append(entry)
    save_books(catalog)

    print("✅ Saved:")
    _print_book(entry)


def find_by_title() -> None:
    catalog = load_books()
    needle = input("Search (part of title): ").strip().lower()

    if not needle:
        print("Nothing to search for.")
        return

    hits = [b for b in catalog if needle in b.title.lower()]
    print(f"Matches: {len(hits)}")
    for b in hits:
        _print_book(b)


def remove_book() -> None:
    catalog = load_books()
    mode = input("Remove using (1) ID or (2) exact title? ").strip()

    if mode == "1":
        raw_id = input("Book ID: ").strip()
        if not raw_id.isdigit():
            print("ID must be numeric.")
            return

        target_id = int(raw_id)
        pruned = [b for b in catalog if b.id != target_id]

        if len(pruned) == len(catalog):
            print("No book found with that ID.")
            return

        save_books(pruned)
        print("✅ Removed.")
        return

    if mode == "2":
        exact = input("Exact title: ").strip().lower()
        if not exact:
            print("Title cannot be empty.")
            return

        matches = [b for b in catalog if b.title.lower() == exact]
        if not matches:
            print("No book found with that title.")
            return

        if len(matches) > 1:
            print("More than one book has this title. Pick an ID:")
            for b in matches:
                _print_book(b)

            raw_choice = input("Chosen ID: ").strip()
            if not raw_choice.isdigit():
                print("ID must be numeric.")
                return

            chosen_id = int(raw_choice)
            pruned = [b for b in catalog if b.id != chosen_id]
            if len(pruned) == len(catalog):
                print("Invalid ID.")
                return

            save_books(pruned)
            print("✅ Removed.")
            return

        victim = matches[0].id
        save_books([b for b in catalog if b.id != victim])
        print("✅ Removed.")
        return

    print("Invalid option.")


def main() -> None:
    while True:
        print("\n=== Mini Library ===")
        print("1) Show books")
        print("2) Add book")
        print("3) Search by title")
        print("4) Delete book")
        print("0) Quit")
        pick = input("Select: ").strip()

        if pick == "1":
            show_all(load_books())
        elif pick == "2":
            create_book()
        elif pick == "3":
            find_by_title()
        elif pick == "4":
            remove_book()
        elif pick == "0":
            break
        else:
            print("Unknown choice.")


if __name__ == "__main__":
    main()
