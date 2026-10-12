
from datetime import date, timedelta
from database import get_connection


def issue_book(book_id, student_id, loan_days=14):
    """Issue an available book to a registered student."""

    if loan_days < 1:
        raise ValueError("Loan period must be at least one day.")

    connection = get_connection()

    try:
        # Start a write transaction to protect availability updates.
        connection.execute("BEGIN IMMEDIATE")

        book = connection.execute(
            "SELECT * FROM books WHERE book_id = ?",
            (book_id,)
        ).fetchone()

        student = connection.execute(
            "SELECT * FROM students WHERE student_id = ?",
            (student_id,)
        ).fetchone()

        if book is None:
            print("Book not found.")
            return False

        if student is None:
            print("Student not found.")
            return False

        if book["available_copies"] <= 0:
            print("No copies of this book are available.")
            return False

        issue_date = date.today()
        due_date = issue_date + timedelta(days=loan_days)

        connection.execute(
            """
            INSERT INTO transactions
                (book_id, student_id, issue_date, due_date)
            VALUES (?, ?, ?, ?)
            """,
            (
                book_id,
                student_id,
                issue_date.isoformat(),
                due_date.isoformat()
            )
        )

        connection.execute(
            """
            UPDATE books
            SET available_copies = available_copies - 1
            WHERE book_id = ? AND available_copies > 0
            """,
            (book_id,)
        )

        connection.commit()

        print("Book issued successfully!")
        print(f"Student: {student['name']}")
        print(f"Book: {book['title']}")
        print(f"Issue date: {issue_date}")
        print(f"Due date: {due_date}")

        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def return_book(transaction_id):
    """Return a book using its transaction ID."""

    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        transaction = connection.execute(
            """
            SELECT * FROM transactions
            WHERE transaction_id = ?
            """,
            (transaction_id,)
        ).fetchone()

        if transaction is None:
            print("Transaction not found.")
            return False

        if transaction["return_date"] is not None:
            print("This book has already been returned.")
            return False

        today = date.today().isoformat()

        connection.execute(
            """
            UPDATE transactions
            SET return_date = ?
            WHERE transaction_id = ? AND return_date IS NULL
            """,
            (today, transaction_id)
        )

        connection.execute(
            """
            UPDATE books
            SET available_copies = available_copies + 1
            WHERE book_id = ?
            """,
            (transaction["book_id"],)
        )

        connection.commit()

        print("Book returned successfully!")
        print(f"Return date: {today}")

        if today > transaction["due_date"]:
            due = date.fromisoformat(transaction["due_date"])
            days_late = (date.today() - due).days
            print(f"Book returned {days_late} day(s) late.")

        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def display_active_issues():
    """Display all books that have not yet been returned."""

    connection = get_connection()

    try:
        records = connection.execute(
            """
            SELECT
                t.transaction_id,
                b.title,
                s.name AS student_name,
                t.issue_date,
                t.due_date
            FROM transactions AS t
            JOIN books AS b ON b.book_id = t.book_id
            JOIN students AS s ON s.student_id = t.student_id
            WHERE t.return_date IS NULL
            ORDER BY t.due_date
            """
        ).fetchall()

        if not records:
            print("No active book issues.")
            return records

        print("\n===== ACTIVE BOOK ISSUES =====")

        for record in records:
            print(
                f"Transaction ID: {record['transaction_id']} | "
                f"Book: {record['title']} | "
                f"Student: {record['student_name']} | "
                f"Issued: {record['issue_date']} | "
                f"Due: {record['due_date']}"
            )

        return records

    finally:
        connection.close()


if __name__ == "__main__":
    while True:
        print("\n===== ISSUE / RETURN MENU =====")
        print("1. Issue book")
        print("2. Return book")
        print("3. View active issues")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                book_id = int(input("Enter book ID: "))
                student_id = int(input("Enter student ID: "))
                issue_book(book_id, student_id)

            elif choice == "2":
                display_active_issues()
                transaction_id = int(
                    input("Enter transaction ID to return: ")
                )
                return_book(transaction_id)

            elif choice == "3":
                display_active_issues()

            elif choice == "0":
                break

            else:
                print("Invalid choice.")

        except ValueError as error:
            print(f"Invalid input: {error}")

        except Exception as error:
            print(f"Operation failed: {error}")
