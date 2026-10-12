
from database import get_connection


def register_student(name, department, phone=""):
    """Register a new student in the library system."""

    name = name.strip()
    department = department.strip()
    phone = phone.strip()

    if not name or not department:
        raise ValueError("Student name and department are required.")

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO students (name, department, phone)
            VALUES (?, ?, ?)
            """,
            (name, department, phone)
        )

        connection.commit()

        print(f"Student registered! Student ID: {cursor.lastrowid}")
        return cursor.lastrowid

    finally:
        connection.close()


def display_students():
    """Display all registered students."""

    connection = get_connection()

    try:
        students = connection.execute(
            "SELECT * FROM students ORDER BY student_id"
        ).fetchall()

        if not students:
            print("No students registered.")
            return students

        print("\n===== REGISTERED STUDENTS =====")

        for student in students:
            print(
                f"ID: {student['student_id']} | "
                f"Name: {student['name']} | "
                f"Department: {student['department']} | "
                f"Phone: {student['phone'] or 'Not provided'}"
            )

        return students

    finally:
        connection.close()


def search_students(keyword):
    """Search students by ID, name or department."""

    keyword = str(keyword).strip()

    if not keyword:
        print("Enter a student ID, name or department.")
        return []

    connection = get_connection()

    try:
        if keyword.isdigit():
            students = connection.execute(
                """
                SELECT * FROM students
                WHERE student_id = ?
                   OR name LIKE ?
                   OR department LIKE ?
                ORDER BY student_id
                """,
                (int(keyword), f"%{keyword}%", f"%{keyword}%")
            ).fetchall()
        else:
            students = connection.execute(
                """
                SELECT * FROM students
                WHERE name LIKE ? OR department LIKE ?
                ORDER BY student_id
                """,
                (f"%{keyword}%", f"%{keyword}%")
            ).fetchall()

        for student in students:
            print(
                f"ID: {student['student_id']} | "
                f"Name: {student['name']} | "
                f"Department: {student['department']}"
            )

        if not students:
            print("No matching students found.")

        return students

    finally:
        connection.close()


if __name__ == "__main__":
    while True:
        print("\n===== STUDENT MANAGEMENT =====")
        print("1. Register student")
        print("2. Display students")
        print("3. Search students")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        try:
            if choice == "1":
                name = input("Student name: ")
                department = input("Department: ")
                phone = input("Phone (optional): ")
                register_student(name, department, phone)

            elif choice == "2":
                display_students()

            elif choice == "3":
                search_students(input("Enter ID, name or department: "))

            elif choice == "0":
                break

            else:
                print("Invalid choice.")

        except Exception as error:
            print(f"Operation failed: {error}")
