
import hashlib
import hmac
import secrets

from database import get_connection


# Password hashing settings
ITERATIONS = 600_000


def hash_password(password):
    """Hash a password using PBKDF2 with a random salt."""
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password, stored_hash):
    """Verify a password against its stored hash."""
    try:
        salt_hex, hash_hex = stored_hash.split(":", 1)
        salt = bytes.fromhex(salt_hex)

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            ITERATIONS
        )

        return hmac.compare_digest(
            calculated_hash.hex(),
            hash_hex
        )

    except (ValueError, TypeError):
        return False


def create_initial_librarian():
    """Create a demo librarian account if no users exist."""
    connection = get_connection()

    try:
        existing_user = connection.execute(
            "SELECT user_id FROM users LIMIT 1"
        ).fetchone()

        if existing_user:
            return

        username = "admin"
        password = "Library@123"
        password_hash = hash_password(password)

        connection.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (username, password_hash, "librarian")
        )

        connection.commit()

        print("Initial librarian account created.")
        print("Username: admin")
        print("Password: Library@123")
        print("Change this demo password before real use.")

    finally:
        connection.close()


def login(username, password):
    """Authenticate a librarian and return True or False."""
    connection = get_connection()

    try:
        user = connection.execute(
            """
            SELECT password_hash, role
            FROM users
            WHERE username = ?
            """,
            (username.strip(),)
        ).fetchone()

        if user is None:
            return False

        if user["role"] != "librarian":
            return False

        return verify_password(password, user["password_hash"])

    finally:
        connection.close()


if __name__ == "__main__":
    create_initial_librarian()

    print("\nTesting login:")

    username = input("Username: ")
    password = input("Password: ")

    if login(username, password):
        print("Login successful!")
    else:
        print("Invalid username or password.")
