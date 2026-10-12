
from database import get_connection


def add_book(title, author, category, total_copies):
    """Add a new book to the library."""

    title = title.strip()
    author = author.strip()
    category = category.strip()

    if not title or not author:
        raise ValueError("Title and author are required.")

    if not isinstance(total_copies, int) or isinstance(total_copies, bool):
        raise ValueError("Number of copies must be a whole number.")

    if total_copies <= 0:
        raise ValueError("Number of copies must be greater than zero.")

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO books
                (title, author, category, total_copies, available_copies)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, author, category, total_copies, total_copies)
        )

        connection.commit()
        print(f"Book added successfully! Book ID: {cursor.lastrowid}")
        return cursor.lastrowid

    finally:
        connection.close()


def delete_book(book_id):
    """Delete a book only if it has no borrowing history."""

    connection = get_connection()

    try:
        book = connection.execute(
            "SELECT book_id FROM books WHERE book_id = ?",
            (book_id,)
        ).fetchone()

        if book is None:
            print("Book not found.")
            return False

        history = connection.execute(
            "SELECT transaction_id FROM transactions WHERE book_id = ? LIMIT 1",
            (book_id,)
        ).fetchone()

        if history is not None:
            print("Cannot delete: this book has borrowing history.")
            return False

        connection.execute(
            "DELETE FROM books WHERE book_id = ?",
            (book_id,)
        )

        connection.commit()
        print("Book deleted successfully!")
        return True

    finally:
        connection.close()


def display_books():
    """Display all books in the library."""

    connection = get_connection()

    try:
        books = connection.execute(
            "SELECT * FROM books ORDER BY book_id"
        ).fetchall()

        if not books:
            print("No books available.")
            return books

        print("\n" + "-" * 95)
        print(
            f"{'ID':<5} {'Title':<25} {'Author':<20} "
            f"{'Category':<15} {'Total':<8} {'Available':<10}"
        )
        print("-" * 95)

        for book in books:
            print(
                f"{book['book_id']:<5} "
                f"{book['title'][:24]:<25} "
                f"{book['author'][:19]:<20} "
                f"{(book['category'] or '')[:14]:<15} "
                f"{book['total_copies']:<8} "
                f"{book['available_copies']:<10}"
            )

        print("-" * 95)
        return books

    finally:
        connection.close()


def search_books(keyword):
    """Search books by ID, title or author."""

    keyword = str(keyword).strip()

    if not keyword:
        print("Please enter a search term.")
        return []

    connection = get_connection()

    try:
        if keyword.isdigit():
            books = connection.execute(
                """
                SELECT * FROM books
                WHERE book_id = ?
                   OR title LIKE ?
                   OR author LIKE ?
                ORDER BY book_id
                """,
                (int(keyword), f"%{keyword}%", f"%{keyword}%")
            ).fetchall()
        else:
            books = connection.execute(
                """
                SELECT * FROM books
                WHERE title LIKE ? OR author LIKE ?
                ORDER BY book_id
                """,
                (f"%{keyword}%", f"%{keyword}%")
            ).fetchall()

        if not books:
            print("No matching books found.")
        else:
            print(f"\nFound {len(books)} matching book(s):")
            for book in books:
                print(
                    f"ID: {book['book_id']} | "
                    f"Title: {book['title']} | "
                    f"Author: {book['author']} | "
                    f"Category: {book['category'] or ''} | "
                    f"Available: {book['available_copies']}"
                )

        return books

    finally:
        connection.close()


if __name__ == "__main__":
    while True:
        print("\n===== BOOK MANAGEMENT TEST MENU =====")
        print("1. Add book")
        print("2. Delete book")
        print("3. Display all books")
        print("4. Search books")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                title = input("Book title: ")
                author = input("Author: ")
                category = input("Category: ")
                copies = int(input("Number of copies: "))

                add_book(title, author, category, copies)

            elif choice == "2":
                book_id = int(input("Enter book ID to delete: "))
                delete_book(book_id)

            elif choice == "3":
                display_books()

            elif choice == "4":
                keyword = input("Enter book ID, title or author: ")
                search_books(keyword)

            elif choice == "0":
                print("Exiting book management test.")
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError as error:
            print(f"Invalid input: {error}")

        except Exception as error:
            print(f"Operation failed: {error}")
    