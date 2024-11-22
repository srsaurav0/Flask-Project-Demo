import os
import ast
from werkzeug.security import check_password_hash

USER_DATA_FILE = os.path.join(os.path.dirname(__file__), "../user_data.py")


def load_users():
    """
    Load users from the user_data.py file.
    """
    try:
        with open(USER_DATA_FILE, "r") as file:
            content = file.read()
            return ast.literal_eval(content.split("=", 1)[1].strip())
    except (FileNotFoundError, SyntaxError, ValueError):
        return []


def save_users(users):
    """
    Save the users list to the user_data.py file.
    """
    with open(USER_DATA_FILE, "w") as file:
        file.write(f"users = {users}")


def find_user_by_email(email):
    """
    Find a user by email.
    """
    users = load_users()
    return next((user for user in users if user["email"] == email), None)


def add_user(user_data):
    """
    Add a new user to the database.
    """
    users = load_users()
    users.append(user_data)
    save_users(users)
    return user_data


def validate_password(stored_password, provided_password):
    """
    Validate a user's password.
    """
    return check_password_hash(stored_password, provided_password)
