import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from views.user import user_blueprint
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    """
    Create a Flask app for testing.
    """
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret-key"
    JWTManager(app)
    app.register_blueprint(user_blueprint)
    return app


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask app.
    """
    return app.test_client()


@pytest.fixture
def mock_user_data(mocker):
    """
    Mock user data and prevent overwriting the actual data file.
    """
    test_users = [
        {
            "email": "user@example.com",
            "name": "Test User",
            "password": generate_password_hash("password_user"),
            "role": "User",
        },
        {
            "email": "admin@example.com",
            "name": "Admin User",
            "password": generate_password_hash("password_admin"),
            "role": "Admin",
        },
    ]

    mocker.patch("models.user.load_users", return_value=test_users)

    mocker.patch("models.user.save_users")


@pytest.fixture
def admin_token(app):
    """
    Generate a valid admin JWT token.
    """
    with app.test_request_context():
        return create_access_token(
            identity="admin@example.com", additional_claims={"role": "Admin"}
        )


@pytest.fixture
def user_token(app):
    """
    Generate a valid user JWT token.
    """
    with app.test_request_context():
        return create_access_token(
            identity="user@example.com", additional_claims={"role": "User"}
        )


def test_register_success(client, mock_user_data):
    """
    Test successful user registration.
    """
    response = client.post(
        "/register",
        json={
            "email": "newuser@example.com",
            "password": "newpassword",
            "name": "New User",
            "role": "User",
        },
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"


def test_register_missing_fields(client):
    """
    Test user registration with missing fields.
    """
    response = client.post("/register", json={"email": "missing@example.com"})
    assert response.status_code == 400
    assert "Missing fields" in response.get_json()["error"]


def test_register_duplicate_email(client, mock_user_data):
    """
    Test user registration with duplicate email.
    """
    response = client.post(
        "/register",
        json={
            "email": "user@example.com",
            "password": "duplicate",
            "name": "Duplicate User",
            "role": "User",
        },
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Email already registered"


def test_login_success(client, mock_user_data):
    """
    Test successful user login.
    """
    response = client.post(
        "/login",
        json={
            "email": "user@example.com",
            "password": "password_user",
        },
    )
    assert response.status_code == 200
    assert "token" in response.get_json()


def test_login_invalid_credentials(client, mock_user_data):
    """
    Test login with invalid credentials.
    """
    response = client.post(
        "/login",
        json={"email": "user@example.com", "password": "wrong_password"},
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid credentials"


def test_login_missing_credentials(client):
    """
    Test login with missing credentials.
    """
    response = client.post("/login", json={"email": "user@example.com"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Email and password are required"


def test_profile_unauthorized(client):
    """
    Test accessing the profile endpoint without a token.
    """
    response = client.get("/profile")
    assert response.status_code == 401
    assert response.get_json().get("msg") == "Missing Authorization Header"


def test_profile_access(client, user_token, mock_user_data):
    """
    Test accessing the profile endpoint with a valid token.
    """
    response = client.get(
        "/profile",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    profile = response.get_json()
    assert profile["email"] == "user@example.com"
    assert profile["role"] == "User"
