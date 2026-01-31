# Mini Library

## Project Overview
This project is a **simple Mini Library Management System** implemented in **Python**.  
It allows users to manage a collection of books by adding, searching, and deleting them.  
All data is stored **persistently** using a JSON file.

The project was developed as a team assignment to practice:
- Git & GitHub
- Branching strategy
- Pull Requests & Code Review
- Issue tracking
- Merge conflict resolution
- Team collaboration

---

## Features
- Add a book (title, author, year)
- Search books by partial title
- Delete books by ID or exact title
- Persistent storage using `books.json`
- CLI interface
- Bonus: Graphical UI using Streamlit

---

## Prerequisites
Make sure the following tools are installed on your system:

- Python 3.10 or higher
- Git
- (For bonus UI) Streamlit

---

## Installation & Run (Step-by-step)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Arshia-mn82/MiniLibrary.git
cd MiniLibrary

```

### Bonus UI (Streamlit)
To run the UI:

```bash
pip install -r requirements.txt

streamlit run ui/app_streamlit.py



### CLI (Terminal)
Run the command-line version from the project root:
```bash
python -m src.app
```
