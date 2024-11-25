import pytest
from controllers.user import register_user, authenticate_user, fetch_profile
from models.user import load_users, save_users
from werkzeug.security import generate_password_hash


@pytest.fixture
def setup_user_data():
    """
    Fixture to set up a clean test environment with mock user data.
    """
    original_users = load_users()
    test_users = [
        {
            "email": "test@example.com",
            "name": "Test User",
            "password": generate_password_hash("password123"),
            "role": "User",
        },
        {
            "email": "admin@example.com",
            "name": "Admin User",
            "password": generate_password_hash("adminpassword"),
            "role": "Admin",
        },
    ]
    save_users(test_users)

    yield test_users

    save_users(original_users)


def test_register_user_success(setup_user_data):
    """
    Test successful user registration.
    """
    new_user_data = {
        "email": "newuser@example.com",
        "password": "newpassword",
        "name": "New User",
        "role": "User",
    }
    registered_user = register_user(new_user_data)

    assert registered_user["email"] == "newuser@example.com"
    assert registered_user["role"] == "User"
    assert len(load_users()) == 3


def test_register_user_missing_fields(setup_user_data):
    """
    Test user registration with missing fields.
    """
    incomplete_data = {"email": "incomplete@example.com"}
    with pytest.raises(ValueError, match="Missing fields: password, name, role"):
        register_user(incomplete_data)


def test_register_user_invalid_role(setup_user_data):
    """
    Test user registration with an invalid role.
    """
    invalid_role_data = {
        "email": "invalidrole@example.com",
        "password": "password",
        "name": "Invalid Role User",
        "role": "Manager",
    }
    with pytest.raises(ValueError, match="Invalid role. Allowed roles: User, Admin"):
        register_user(invalid_role_data)


def test_register_user_duplicate_email(setup_user_data):
    """
    Test user registration with a duplicate email.
    """
    duplicate_email_data = {
        "email": "test@example.com",
        "password": "password",
        "name": "Duplicate User",
        "role": "User",
    }
    with pytest.raises(ValueError, match="Email already registered"):
        register_user(duplicate_email_data)


def test_authenticate_user_success(setup_user_data):
    """
    Test successful user authentication.
    """
    credentials = {"email": "test@example.com", "password": "password123"}
    user = authenticate_user(credentials)
    assert user["email"] == "test@example.com"
    assert user["role"] == "User"


def test_authenticate_user_invalid_credentials(setup_user_data):
    """
    Test user authentication with invalid credentials.
    """
    invalid_credentials = {"email": "test@example.com", "password": "wrongpassword"}
    with pytest.raises(ValueError, match="Invalid credentials"):
        authenticate_user(invalid_credentials)


def test_authenticate_user_missing_credentials(setup_user_data):
    """
    Test user authentication with missing credentials.
    """
    with pytest.raises(ValueError, match="Email and password are required"):
        authenticate_user({"email": "test@example.com"})


def test_fetch_profile_success(setup_user_data):
    """
    Test fetching a user profile successfully.
    """
    profile = fetch_profile("test@example.com")
    assert profile == {"email": "test@example.com", "role": "User"}


def test_fetch_profile_user_not_found(setup_user_data):
    """
    Test fetching a profile for a non-existent user.
    """
    with pytest.raises(ValueError, match="User not found"):
        fetch_profile("nonexistent@example.com")
