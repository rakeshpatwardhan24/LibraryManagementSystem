
import sqlite3

DB_NAME = "library.db"


def get_connection():
    """Create a connection to the library database."""
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create all tables required by the library system."""

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'librarian'
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                phone TEXT
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                category TEXT,
                total_copies INTEGER NOT NULL
                    CHECK (total_copies >= 0),
                available_copies INTEGER NOT NULL
                    CHECK (
                        available_copies >= 0
                        AND available_copies <= total_copies
                    )
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                issue_date TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books(book_id)
                    ON DELETE RESTRICT,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
                    ON DELETE RESTRICT
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_books_title
            ON books(title)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_books_author
            ON books(author)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_student
            ON transactions(student_id)
        """)

    print("Database initialized successfully!")


if __name__ == "__main__":
    initialize_database()
