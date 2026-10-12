# Library Management System

## 1. Project Overview

The **Library Management System** is a Python desktop application
designed to help a librarian manage books, students, book issue/return
transactions, and library reports. It uses Tkinter for the graphical
user interface and SQLite for persistent storage.

## 2. Problem Statement

Manual library records can be difficult to maintain and search. This
project provides a simple centralized application to manage book
inventory, student records, borrowing activity, and reports while
reducing errors in tracking available copies.

## 3. Objectives

-   Maintain book and student records in a database.
-   Support adding, deleting, displaying, and searching books.
-   Register students and search student records.
-   Issue available books and record due dates.
-   Process returns and update available-copy counts.
-   Display inventory, active-issue, overdue, and transaction-history
    reports.
-   Provide a graphical interface with librarian login.

## 4. Functional Requirements

1.  **Login module:** Authenticate the librarian.
2.  **Book management:** Add, delete, display, and search books.
3.  **Student/user management:** Register, display, and search students.
4.  **Issue/return module:** Issue available books, record due dates,
    process returns, and maintain transaction history.
5.  **Search module:** Search books and students by supported
    identifiers or text fields.
6.  **Report module:** Display inventory, active issues, overdue books,
    and transaction history.

## 5. Non-Functional Requirements

-   **Performance:** SQLite queries and indexes support efficient common
    searches.
-   **Reliability:** Input checks, database constraints, and
    transactions help preserve consistent records.
-   **Security:** Passwords are stored as salted PBKDF2 hashes, and SQL
    queries use parameters.
-   **Maintainability:** Functionality is separated into modules.
-   **Scalability:** The normalized relational schema is suitable for a
    small library; larger deployments may need a server database.
-   **Usability:** Tkinter provides a graphical interface with tabs,
    tables, and confirmation/error messages.

## 6. Technologies Used

-   Python 3
-   Tkinter (`tkinter` and `ttk`)
-   SQLite (`sqlite3`)
-   `hashlib`, `hmac`, `secrets`, and other Python standard-library
    modules
-   Visual Studio Code

No third-party Python packages are required for the current
implementation.

## 7. Project File Structure

``` text
LibraryManagementSystem/
├── main.py
├── database.py
├── auth.py
├── book_manager.py
├── student_manager.py
├── transactions.py
├── reports.py
├── library.db          # Created automatically
└── README.md
```

## 8. Module Description

  -----------------------------------------------------------------------
  File                                Responsibility
  ----------------------------------- -----------------------------------
  `main.py`                           Tkinter application, login screen,
                                      dashboard, and GUI actions

  `database.py`                       SQLite connection and table/index
                                      initialization

  `auth.py`                           Password hashing, password
                                      verification, and librarian login

  `book_manager.py`                   Add, delete, display, and search
                                      books

  `student_manager.py`                Register, display, and search
                                      students

  `transactions.py`                   Issue books, return books, and list
                                      active issues

  `reports.py`                        Inventory, active-issue, overdue,
                                      and transaction-history reports
  -----------------------------------------------------------------------

## 9. Database Design

The application uses four tables:

-   **users:** `user_id`, `username`, `password_hash`, `role`
-   **students:** `student_id`, `name`, `department`, `phone`
-   **books:** `book_id`, `title`, `author`, `category`, `total_copies`,
    `available_copies`
-   **transactions:** `transaction_id`, `book_id`, `student_id`,
    `issue_date`, `due_date`, `return_date`

Primary keys uniquely identify records. Foreign keys connect
transactions to books and students. Constraints prevent negative copy
counts and available copies exceeding total copies.

## 10. Setup and Execution

1.  Install Python 3 and Visual Studio Code if they are not already
    installed.

2.  Open the `LibraryManagementSystem` folder in VS Code.

3.  Open **Terminal → New Terminal**.

4.  Initialize the database:

    ``` powershell
    python database.py
    ```

5.  Create the initial demo librarian account if no user exists:

    ``` powershell
    python auth.py
    ```

    Follow the prompts to test login. The initial demo account created
    by the current code is `admin` with password `Library@123`, unless
    an account already exists.

6.  Launch the complete GUI:

    ``` powershell
    python main.py
    ```

The database file is created in the application's current working
directory. Run commands from the project folder to use the expected
`library.db`.

## 11. Test Plan and Results

The following tests were reported as passing during project testing:

  -----------------------------------------------------------------------
  Test area               Test                    Expected result
  ----------------------- ----------------------- -----------------------
  Authentication          Correct credentials     Dashboard opens

  Authentication          Incorrect credentials   Login rejected

  Book management         Add and display book    Book appears with
                                                  correct copy counts

  Book management         Search by text or ID    Matching books are
                                                  displayed

  Book management         Delete a book without   Book is removed after
                          transaction history     confirmation

  Book management         Delete a book with      Deletion is refused
                          transaction history     

  Student management      Register and search     Student record is saved
                          student                 and found

  Issue/return            Issue an available book Available-copy count
                                                  decreases

  Issue/return            Issue when no copies    Operation is rejected
                          are available           

  Issue/return            Return a book           Return date is saved
                                                  and availability
                                                  increases

  Issue/return            Return the same         Duplicate return is
                          transaction twice       rejected

  Reports                 Run all four reports    Appropriate records and
                                                  totals are displayed
  -----------------------------------------------------------------------

## 12. Demonstration Sequence

For a short project demonstration:

1.  Launch `main.py` and log in.
2.  Add a test book and search for it.
3.  Register a test student.
4.  Issue the book and show the reduced available-copy count.
5.  Return the book and show the restored count.
6.  Open the inventory and transaction-history reports.
7.  Demonstrate that a book with borrowing history cannot be deleted.
8.  Log out.

Use test records during the demonstration and preserve the database
containing any records you need.

## 13. Security and Data Notes

-   The default credentials are for demonstration only. Change the
    password mechanism before using the application with real users.
-   Do not publish `library.db` if it contains real student information
    or password hashes.
-   The current application is a local, single-librarian demonstration,
    not a hardened multi-user production system.
-   Back up the database before making schema or data changes.

## 14. Limitations and Future Enhancements

-   Add a GUI-based password-change feature and remove the hard-coded
    demo password.
-   Add role-based access for multiple librarians.
-   Add fine calculation and configurable loan periods.
-   Add report export to CSV or PDF.
-   Add automated database backups.
-   Consider a server database and concurrent-user support if the system
    grows.

## 15. Conclusion

The Library Management System demonstrates the use of Python, Tkinter,
SQLite, modular programming, database constraints, password hashing, and
transaction handling to implement common library workflows in a desktop
application.
