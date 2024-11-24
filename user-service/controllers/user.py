from models.user import (
    find_user_by_email,
    add_user,
    validate_password,
)
from werkzeug.security import generate_password_hash


def register_user(data):
    """
    Controller to validate and register a new user.
    """
    required_fields = ["email", "password", "name", "role"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        raise ValueError(f"Missing fields: {', '.join(missing_fields)}")

    # Validate role
    valid_roles = ["User", "Admin"]
    if data["role"] not in valid_roles:
        raise ValueError(f"Invalid role. Allowed roles: {', '.join(valid_roles)}")

    # Check if email is already registered
    if find_user_by_email(data["email"]):
        raise ValueError("Email already registered")

    # Add the new user
    hashed_password = generate_password_hash(data["password"])
    return add_user(
        {
            "email": data["email"],
            "name": data["name"],
            "password": hashed_password,
            "role": data["role"],
        }
    )


def authenticate_user(data):
    """
    Controller to authenticate a user.
    """
    if not data or "email" not in data or "password" not in data:
        raise ValueError("Email and password are required")

    user = find_user_by_email(data["email"])
    if not user or not validate_password(user["password"], data["password"]):
        raise ValueError("Invalid credentials")

    return user


def fetch_profile(email):
    """
    Controller to fetch a user's profile.
    """
    user = find_user_by_email(email)
    if not user:
        raise ValueError("User not found")
    return {"email": user["email"], "role": user["role"]}
