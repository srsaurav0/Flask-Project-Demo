import os
import pytest
from werkzeug.security import generate_password_hash
from models.user import (
    load_users,
    save_users,
    find_user_by_email,
    add_user,
    validate_password,
)

# Path to a temporary user_data.py for testing
TEST_USER_DATA_FILE = os.path.join(os.path.dirname(__file__), "test_user_data.py")

# Path to the actual user_data.py
USER_DATA_FILE = os.path.join(os.path.dirname(__file__), "../user_data.py")


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Set up a clean test environment by backing up the original user_data.py
    and restoring it after the tests.
    """
    # Backup the original user_data.py file
    if os.path.exists(USER_DATA_FILE):
        os.rename(USER_DATA_FILE, f"{USER_DATA_FILE}.bak")

    try:
        # Create a clean user_data.py file for testing
        with open(USER_DATA_FILE, "w") as file:
            file.write("users = []")

        yield  # Run the tests

    finally:
        # Restore the original user_data.py after tests
        if os.path.exists(f"{USER_DATA_FILE}.bak"):
            os.rename(f"{USER_DATA_FILE}.bak", USER_DATA_FILE)


def test_load_users_empty():
    """
    Test loading users from an empty user_data.py file.
    """
    users = load_users()
    assert users == []


def test_save_and_load_users():
    """
    Test saving and loading users.
    """
    users = [
        {
            "email": "test@example.com",
            "name": "Test User",
            "password": "hashed_password",
        }
    ]
    save_users(users)

    loaded_users = load_users()
    assert loaded_users == users


def test_find_user_by_email():
    """
    Test finding a user by email.
    """
    users = [
        {
            "email": "test@example.com",
            "name": "Test User",
            "password": "hashed_password",
        }
    ]
    save_users(users)

    user = find_user_by_email("test@example.com")
    assert user is not None
    assert user["email"] == "test@example.com"
    assert user["name"] == "Test User"


def test_add_user():
    """
    Test adding a new user.
    """
    user_data = {
        "email": "new@example.com",
        "name": "New User",
        "password": "hashed_password",
    }
    added_user = add_user(user_data)

    users = load_users()
    assert len(users) == 1
    assert users[0] == user_data
    assert added_user == user_data


def test_validate_password():
    """
    Test validating a user's password.
    """
    hashed_password = generate_password_hash("my_password")
    assert validate_password(hashed_password, "my_password") is True
    assert validate_password(hashed_password, "wrong_password") is False
