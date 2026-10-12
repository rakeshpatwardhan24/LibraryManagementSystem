
from datetime import date
from database import get_connection


def inventory_report():
    """Show total books, copies and available copies."""

    connection = get_connection()

    try:
        summary = connection.execute("""
            SELECT
                COUNT(*) AS title_count,
                COALESCE(SUM(total_copies), 0) AS total_copies,
                COALESCE(SUM(available_copies), 0) AS available_copies
            FROM books
        """).fetchone()

        print("\n===== INVENTORY REPORT =====")
        print(f"Different book titles: {summary['title_count']}")
        print(f"Total physical copies: {summary['total_copies']}")
        print(f"Available copies: {summary['available_copies']}")
        print(
            f"Currently issued copies: "
            f"{summary['total_copies'] - summary['available_copies']}"
        )

        return summary

    finally:
        connection.close()


def active_issues_report():
    """Show books that have not been returned."""

    connection = get_connection()

    try:
        records = connection.execute("""
            SELECT
                t.transaction_id,
                b.title,
                s.name AS student_name,
                t.issue_date,
                t.due_date
            FROM transactions t
            JOIN books b ON b.book_id = t.book_id
            JOIN students s ON s.student_id = t.student_id
            WHERE t.return_date IS NULL
            ORDER BY t.due_date
        """).fetchall()

        print("\n===== ACTIVE ISSUES REPORT =====")

        if not records:
            print("No active issues.")
        else:
            for record in records:
                print(
                    f"Transaction ID: {record['transaction_id']} | "
                    f"Book: {record['title']} | "
                    f"Student: {record['student_name']} | "
                    f"Due: {record['due_date']}"
                )

        return records

    finally:
        connection.close()


def overdue_report():
    """Show books that are past their due date."""

    connection = get_connection()

    try:
        today = date.today().isoformat()

        records = connection.execute("""
            SELECT
                t.transaction_id,
                b.title,
                s.name AS student_name,
                t.due_date
            FROM transactions t
            JOIN books b ON b.book_id = t.book_id
            JOIN students s ON s.student_id = t.student_id
            WHERE t.return_date IS NULL
              AND t.due_date < ?
            ORDER BY t.due_date
        """, (today,)).fetchall()

        print("\n===== OVERDUE BOOKS REPORT =====")

        if not records:
            print("No overdue books.")
        else:
            for record in records:
                due = date.fromisoformat(record["due_date"])
                days_late = (date.today() - due).days

                print(
                    f"Transaction ID: {record['transaction_id']} | "
                    f"Book: {record['title']} | "
                    f"Student: {record['student_name']} | "
                    f"Days overdue: {days_late}"
                )

        return records

    finally:
        connection.close()


def transaction_history_report():
    """Show completed and active borrowing transactions."""

    connection = get_connection()

    try:
        records = connection.execute("""
            SELECT
                t.transaction_id,
                b.title,
                s.name AS student_name,
                t.issue_date,
                t.due_date,
                t.return_date
            FROM transactions t
            JOIN books b ON b.book_id = t.book_id
            JOIN students s ON s.student_id = t.student_id
            ORDER BY t.transaction_id DESC
        """).fetchall()

        print("\n===== TRANSACTION HISTORY =====")

        if not records:
            print("No transactions recorded.")
        else:
            for record in records:
                status = (
                    f"Returned on {record['return_date']}"
                    if record["return_date"]
                    else "Not returned"
                )

                print(
                    f"ID: {record['transaction_id']} | "
                    f"Book: {record['title']} | "
                    f"Student: {record['student_name']} | "
                    f"Issued: {record['issue_date']} | "
                    f"Due: {record['due_date']} | "
                    f"Status: {status}"
                )

        return records

    finally:
        connection.close()


if __name__ == "__main__":
    while True:
        print("\n===== LIBRARY REPORTS =====")
        print("1. Inventory report")
        print("2. Active issues report")
        print("3. Overdue books report")
        print("4. Transaction history")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                inventory_report()
            elif choice == "2":
                active_issues_report()
            elif choice == "3":
                overdue_report()
            elif choice == "4":
                transaction_history_report()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

        except Exception as error:
            print(f"Report failed: {error}")
