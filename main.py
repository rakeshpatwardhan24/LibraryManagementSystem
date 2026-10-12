
import tkinter as tk
from tkinter import ttk, messagebox

from auth import login, create_initial_librarian
from database import get_connection
from book_manager import add_book, delete_book, display_books, search_books
from student_manager import (
    register_student, display_students, search_students
)
from transactions import issue_book, return_book, display_active_issues
from reports import (
    inventory_report,
    active_issues_report,
    overdue_report,
    transaction_history_report
)


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1050x700")
        self.root.minsize(850, 600)

        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=27)
        self.style.configure("TButton", padding=5)

        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- LOGIN ----------------

    def show_login(self):
        self.clear_window()

        frame = ttk.Frame(self.root, padding=35)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(
            frame, text="LIBRARY MANAGEMENT SYSTEM",
            font=("Segoe UI", 19, "bold")
        ).pack(pady=(0, 8))

        ttk.Label(
            frame, text="Librarian Login",
            font=("Segoe UI", 12)
        ).pack(pady=(0, 20))

        ttk.Label(frame, text="Username").pack(anchor="w")
        self.username_entry = ttk.Entry(frame, width=35)
        self.username_entry.pack(pady=(4, 12))

        ttk.Label(frame, text="Password").pack(anchor="w")
        self.password_entry = ttk.Entry(frame, width=35, show="*")
        self.password_entry.pack(pady=(4, 16))

        ttk.Button(
            frame, text="Login", command=self.handle_login
        ).pack(fill="x")

        self.password_entry.bind(
            "<Return>", lambda event: self.handle_login()
        )
        self.username_entry.focus_set()

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            if login(username, password):
                self.show_dashboard()
            else:
                messagebox.showerror(
                    "Login Failed", "Invalid username or password."
                )
        except Exception as error:
            messagebox.showerror("Error", str(error))

    # ---------------- DASHBOARD ----------------

    def show_dashboard(self):
        self.clear_window()

        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")

        ttk.Label(
            header, text="Library Management System",
            font=("Segoe UI", 18, "bold")
        ).pack(side="left")

        ttk.Button(
            header, text="Logout", command=self.show_login
        ).pack(side="right")

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=8)

        self.book_tab = ttk.Frame(self.tabs, padding=12)
        self.student_tab = ttk.Frame(self.tabs, padding=12)
        self.transaction_tab = ttk.Frame(self.tabs, padding=12)
        self.report_tab = ttk.Frame(self.tabs, padding=12)

        self.tabs.add(self.book_tab, text="Books")
        self.tabs.add(self.student_tab, text="Students")
        self.tabs.add(self.transaction_tab, text="Issue / Return")
        self.tabs.add(self.report_tab, text="Reports")

        self.build_books_tab()
        self.build_students_tab()
        self.build_transactions_tab()
        self.build_reports_tab()

    # ---------------- BOOK MANAGEMENT ----------------

    def build_books_tab(self):
        tab = self.book_tab

        ttk.Label(
            tab, text="Book Management",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        form = ttk.Frame(tab)
        form.pack(fill="x")

        self.book_title = self.add_field(form, "Title", 0, 0)
        self.book_author = self.add_field(form, "Author", 0, 2)
        self.book_category = self.add_field(form, "Category", 1, 0)
        self.book_copies = self.add_field(form, "Copies", 1, 2)

        buttons = ttk.Frame(tab)
        buttons.pack(fill="x", pady=10)

        ttk.Button(
            buttons, text="Add Book", command=self.add_book_action
        ).pack(side="left", padx=3)

        ttk.Button(
            buttons, text="Delete Selected",
            command=self.delete_book_action
        ).pack(side="left", padx=3)

        ttk.Button(
            buttons, text="Display All",
            command=self.load_books
        ).pack(side="left", padx=3)

        self.book_search = ttk.Entry(buttons, width=22)
        self.book_search.pack(side="left", padx=(15, 3))

        ttk.Button(
            buttons, text="Search",
            command=self.search_book_action
        ).pack(side="left", padx=3)

        columns = (
            "id", "title", "author", "category", "total", "available"
        )
        self.book_tree = self.create_tree(tab, columns, {
            "id": ("ID", 45),
            "title": ("Title", 220),
            "author": ("Author", 170),
            "category": ("Category", 130),
            "total": ("Total", 70),
            "available": ("Available", 90)
        })

        self.load_books()

    def add_book_action(self):
        try:
            copies = int(self.book_copies.get())

            add_book(
                self.book_title.get(),
                self.book_author.get(),
                self.book_category.get(),
                copies
            )

            messagebox.showinfo("Success", "Book added successfully.")
            self.load_books()

        except (ValueError, Exception) as error:
            messagebox.showerror("Unable to Add Book", str(error))

    def load_books(self):
        try:
            books = display_books()
            self.clear_tree(self.book_tree)

            for book in books:
                self.book_tree.insert("", "end", values=(
                    book["book_id"], book["title"], book["author"],
                    book["category"] or "", book["total_copies"],
                    book["available_copies"]
                ))
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def search_book_action(self):
        try:
            books = search_books(self.book_search.get())
            self.clear_tree(self.book_tree)

            for book in books:
                self.book_tree.insert("", "end", values=(
                    book["book_id"], book["title"], book["author"],
                    book["category"] or "", book["total_copies"],
                    book["available_copies"]
                ))
        except Exception as error:
            messagebox.showerror("Search Error", str(error))

    def delete_book_action(self):
        selected = self.book_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Book", "Select a book from the table first."
            )
            return

        book_id = int(self.book_tree.item(selected[0], "values")[0])

        if messagebox.askyesno(
            "Confirm Delete",
            f"Delete book ID {book_id}? This cannot be undone."
        ):
            try:
                if delete_book(book_id):
                    messagebox.showinfo("Success", "Book deleted.")
                else:
                    messagebox.showwarning(
                        "Not Deleted",
                        "Book not found or has borrowing history."
                    )
                self.load_books()
            except Exception as error:
                messagebox.showerror("Delete Error", str(error))

    # ---------------- STUDENT MANAGEMENT ----------------

    def build_students_tab(self):
        tab = self.student_tab

        ttk.Label(
            tab, text="Student Management",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        form = ttk.Frame(tab)
        form.pack(fill="x")

        self.student_name = self.add_field(form, "Student Name", 0, 0)
        self.student_department = self.add_field(
            form, "Department", 0, 2
        )
        self.student_phone = self.add_field(
            form, "Phone (optional)", 1, 0
        )

        buttons = ttk.Frame(tab)
        buttons.pack(fill="x", pady=10)

        ttk.Button(
            buttons, text="Register Student",
            command=self.register_student_action
        ).pack(side="left", padx=3)

        ttk.Button(
            buttons, text="Display All",
            command=self.load_students
        ).pack(side="left", padx=3)

        self.student_search = ttk.Entry(buttons, width=24)
        self.student_search.pack(side="left", padx=(15, 3))

        ttk.Button(
            buttons, text="Search",
            command=self.search_student_action
        ).pack(side="left", padx=3)

        columns = ("id", "name", "department", "phone")
        self.student_tree = self.create_tree(tab, columns, {
            "id": ("Student ID", 90),
            "name": ("Name", 230),
            "department": ("Department", 180),
            "phone": ("Phone", 150)
        })

        self.load_students()

    def register_student_action(self):
        try:
            register_student(
                self.student_name.get(),
                self.student_department.get(),
                self.student_phone.get()
            )

            messagebox.showinfo(
                "Success", "Student registered successfully."
            )
            self.load_students()

        except Exception as error:
            messagebox.showerror("Registration Error", str(error))

    def load_students(self):
        try:
            students = display_students()
            self.clear_tree(self.student_tree)

            for student in students:
                self.student_tree.insert("", "end", values=(
                    student["student_id"], student["name"],
                    student["department"], student["phone"] or ""
                ))
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def search_student_action(self):
        try:
            students = search_students(self.student_search.get())
            self.clear_tree(self.student_tree)

            for student in students:
                self.student_tree.insert("", "end", values=(
                    student["student_id"], student["name"],
                    student["department"], student["phone"] or ""
                ))
        except Exception as error:
            messagebox.showerror("Search Error", str(error))

    # ---------------- ISSUE / RETURN ----------------

    def build_transactions_tab(self):
        tab = self.transaction_tab

        ttk.Label(
            tab, text="Issue and Return Books",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        form = ttk.Frame(tab)
        form.pack(fill="x")

        self.issue_book_id = self.add_field(
            form, "Book ID", 0, 0
        )
        self.issue_student_id = self.add_field(
            form, "Student ID", 0, 2
        )

        buttons = ttk.Frame(tab)
        buttons.pack(fill="x", pady=10)

        ttk.Button(
            buttons, text="Issue Book",
            command=self.issue_book_action
        ).pack(side="left", padx=3)

        ttk.Button(
            buttons, text="Refresh Active Issues",
            command=self.load_active_issues
        ).pack(side="left", padx=3)

        ttk.Label(
            tab, text="Select an active transaction to return its book."
        ).pack(anchor="w", pady=(10, 5))

        ttk.Button(
            tab, text="Return Selected Book",
            command=self.return_book_action
        ).pack(anchor="w", pady=(0, 8))

        columns = (
            "transaction", "book", "student", "issued", "due"
        )
        self.issue_tree = self.create_tree(tab, columns, {
            "transaction": ("Transaction ID", 110),
            "book": ("Book", 240),
            "student": ("Student", 200),
            "issued": ("Issue Date", 120),
            "due": ("Due Date", 120)
        })

        self.load_active_issues()

    def issue_book_action(self):
        try:
            book_id = int(self.issue_book_id.get())
            student_id = int(self.issue_student_id.get())

            if issue_book(book_id, student_id):
                messagebox.showinfo(
                    "Success", "Book issued successfully."
                )
                self.load_active_issues()
                self.load_books()
        except Exception as error:
            messagebox.showerror("Issue Error", str(error))

    def load_active_issues(self):
        try:
            connection = get_connection()
            try:
                records = connection.execute("""
                    SELECT t.transaction_id, b.title,
                           s.name AS student_name,
                           t.issue_date, t.due_date
                    FROM transactions t
                    JOIN books b ON b.book_id = t.book_id
                    JOIN students s ON s.student_id = t.student_id
                    WHERE t.return_date IS NULL
                    ORDER BY t.due_date
                """).fetchall()
            finally:
                connection.close()

            self.clear_tree(self.issue_tree)

            for record in records:
                self.issue_tree.insert("", "end", values=(
                    record["transaction_id"], record["title"],
                    record["student_name"], record["issue_date"],
                    record["due_date"]
                ))
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def return_book_action(self):
        selected = self.issue_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Transaction",
                "Select an active issue from the table."
            )
            return

        transaction_id = int(
            self.issue_tree.item(selected[0], "values")[0]
        )

        if messagebox.askyesno(
            "Confirm Return",
            f"Record return for transaction {transaction_id}?"
        ):
            try:
                if return_book(transaction_id):
                    messagebox.showinfo(
                        "Success", "Book returned successfully."
                    )
                self.load_active_issues()
                self.load_books()
            except Exception as error:
                messagebox.showerror("Return Error", str(error))

    # ---------------- REPORTS ----------------

    def build_reports_tab(self):
        tab = self.report_tab

        ttk.Label(
            tab, text="Library Reports",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))

        buttons = ttk.Frame(tab)
        buttons.pack(fill="x", pady=(0, 10))

        options = [
            ("Inventory", inventory_report),
            ("Active Issues", active_issues_report),
            ("Overdue Books", overdue_report),
            ("Transaction History", transaction_history_report)
        ]

        for label, function in options:
            ttk.Button(
                buttons, text=label,
                command=lambda f=function: self.show_report(f)
            ).pack(side="left", padx=3)

        self.report_output = tk.Text(
            tab, wrap="word", height=24,
            font=("Consolas", 10), state="disabled"
        )
        self.report_output.pack(fill="both", expand=True)

    def show_report(self, report_function):
        try:
            # Capture the report's printed output.
            import io
            from contextlib import redirect_stdout

            buffer = io.StringIO()
            with redirect_stdout(buffer):
                report_function()

            output = buffer.getvalue()

            self.report_output.config(state="normal")
            self.report_output.delete("1.0", "end")
            self.report_output.insert("1.0", output)
            self.report_output.config(state="disabled")

        except Exception as error:
            messagebox.showerror("Report Error", str(error))

    # ---------------- SHARED HELPERS ----------------

    def add_field(self, parent, label, row, column):
        frame = ttk.Frame(parent)
        frame.grid(
            row=row, column=column,
            sticky="ew", padx=5, pady=5
        )

        ttk.Label(frame, text=label).pack(anchor="w")
        entry = ttk.Entry(frame, width=27)
        entry.pack(fill="x", pady=(3, 0))
        return entry

    def create_tree(self, parent, columns, headings):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, pady=5)

        tree = ttk.Treeview(
            frame, columns=columns,
            show="headings", selectmode="browse"
        )

        for column in columns:
            title, width = headings[column]
            tree.heading(column, text=title)
            tree.column(column, width=width, anchor="w")

        scrollbar = ttk.Scrollbar(
            frame, orient="vertical", command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return tree

    @staticmethod
    def clear_tree(tree):
        for item in tree.get_children():
            tree.delete(item)


if __name__ == "__main__":
    create_initial_librarian()

    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
