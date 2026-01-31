import streamlit as st
from pathlib import Path
import sys

# Add project root to import path (so we can import src/*)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.models import Book  # noqa: E402
from src.storage import load_books, save_books, next_id  # noqa: E402


st.set_page_config(page_title="Mini Library", page_icon="📚", layout="centered")

# --- Small CSS refresh (purely visual) ---
st.markdown(
    """
    <style>
      .ml-card {
        border: 1px solid rgba(49, 51, 63, 0.18);
        border-radius: 14px;
        padding: 12px 14px;
        margin: 8px 0;
        background: rgba(250, 250, 252, 0.35);
      }
      .ml-muted { opacity: 0.75; font-size: 0.92rem; }
      .ml-title { font-weight: 650; font-size: 1.02rem; }
      .ml-badge {
        display: inline-block; padding: 1px 8px; border-radius: 999px;
        border: 1px solid rgba(49, 51, 63, 0.18); font-size: 0.85rem;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📚 Mini Library")


def book_card(b: Book) -> None:
    st.markdown(
        f"""
        <div class="ml-card">
          <div class="ml-title"><span class="ml-badge">#{b.id}</span> {b.title}</div>
          <div class="ml-muted">{b.author} • {b.year}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Sidebar: quick stats (visual only)
with st.sidebar:
    st.header("Overview")
    all_books = load_books()
    st.metric("Total books", len(all_books))
    st.write("Data file:", "`data/books.json`")


tabs = st.tabs(["➕ Add", "🔎 Search", "🗑️ Delete", "📖 Browse"])

# --- Add ---
with tabs[0]:
    st.subheader("Add a book")
    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            title_in = st.text_input("Title", placeholder="e.g., The Hobbit")
            author_in = st.text_input("Author", placeholder="e.g., J. R. R. Tolkien")
        with c2:
            year_in = st.text_input("Year", placeholder="e.g., 1937")
            st.caption("Year must be a number.")
        submitted = st.form_submit_button("Save")

    if submitted:
        title_s = title_in.strip()
        author_s = author_in.strip()
        year_s = year_in.strip()

        if not title_s:
            st.error("Title cannot be empty.")
        elif not author_s:
            st.error("Author cannot be empty.")
        elif not year_s.isdigit():
            st.error("Year must be a number.")
        else:
            books = load_books()
            new_book = Book(id=next_id(books), title=title_s, author=author_s, year=int(year_s))
            books.append(new_book)
            save_books(books)
            st.success("Saved!")
            book_card(new_book)

# --- Search ---
with tabs[1]:
    st.subheader("Search")
    q = st.text_input("Search by partial title", placeholder="Type a part of the title…").strip().lower()

    col_a, col_b = st.columns([1, 2])
    with col_a:
        do_search = st.button("Search", use_container_width=True)
    with col_b:
        st.caption("Search is case-insensitive and matches anywhere in the title.")

    if do_search:
        books = load_books()
        if not q:
            st.warning("Enter a search query.")
        else:
            found = [b for b in books if q in b.title.lower()]
            st.info(f"Found {len(found)} result(s).")
            for b in found:
                book_card(b)

# --- Delete ---
with tabs[2]:
    st.subheader("Delete")
    books_now = load_books()

    st.write("Choose how you want to delete:")
    mode = st.radio("Mode", ["By ID", "By exact title"], horizontal=True, label_visibility="collapsed")

    if mode == "By ID":
        with st.form("del_by_id"):
            raw = st.text_input("Book ID", placeholder="e.g., 3")
            ok = st.form_submit_button("Delete")
        if ok:
            if not raw.strip().isdigit():
                st.error("ID must be a number.")
            else:
                bid = int(raw.strip())
                updated = [b for b in books_now if b.id != bid]
                if len(updated) == len(books_now):
                    st.warning("No book found with this ID.")
                else:
                    save_books(updated)
                    st.success("Deleted.")

    else:
        with st.form("del_by_title"):
            title_exact = st.text_input("Exact title", placeholder="Must match the full title").strip().lower()
            ok = st.form_submit_button("Find")
        if ok:
            if not title_exact:
                st.error("Title cannot be empty.")
            else:
                candidates = [b for b in books_now if b.title.lower() == title_exact]
                if not candidates:
                    st.warning("No book found with this title.")
                elif len(candidates) == 1:
                    victim = candidates[0].id
                    save_books([b for b in books_now if b.id != victim])
                    st.success("Deleted.")
                else:
                    st.warning("Multiple books match this title. Pick which one to delete:")
                    options = {f"#{b.id} — {b.author} ({b.year})": b.id for b in candidates}
                    label = st.selectbox("Select", list(options.keys()))
                    if st.button("Delete selected", use_container_width=True):
                        chosen = int(options[label])
                        save_books([b for b in books_now if b.id != chosen])
                        st.success("Deleted.")

# --- Browse ---
with tabs[3]:
    st.subheader("All books")
    books = load_books()

    if not books:
        st.info("No books yet.")
    else:
        # purely visual sorting, does not change storage
        order = st.selectbox("Sort by", ["ID (asc)", "Title (A→Z)", "Year (new→old)"])
        if order == "Title (A→Z)":
            books = sorted(books, key=lambda b: b.title.lower())
        elif order == "Year (new→old)":
            books = sorted(books, key=lambda b: b.year, reverse=True)
        else:
            books = sorted(books, key=lambda b: b.id)

        # Show as a table (quick scan) + cards (pretty)
        with st.expander("Table view", expanded=False):
            st.dataframe(
                [{"ID": b.id, "Title": b.title, "Author": b.author, "Year": b.year} for b in books],
                use_container_width=True,
                hide_index=True,
            )

        for b in books:
            book_card(b)
