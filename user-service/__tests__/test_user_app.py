import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash
from views.user import user_blueprint
from flasgger import Swagger


@pytest.fixture
def app():
    """
    Create a Flask app for testing with Swagger and JWT setup.
    """
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "shared-secret-key"
    Swagger(
        app,
        template={
            "swagger": "2.0",
            "info": {
                "title": "User Service API",
                "description": "API for user registration, authentication, and profile management.",
                "version": "1.0.0",
            },
            "host": "127.0.0.1:5002",
            "basePath": "/",
            "schemes": ["http"],
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"',
                }
            },
            "security": [{"Bearer": []}],
        },
    )
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
def setup_test_users(mocker):
    """
    Mock user data for tests.
    """
    test_users = [
        {
            "email": "user@example.com",
            "name": "Test User",
            "password": generate_password_hash("password_user"),  # Hashed password
            "role": "User",
        },
        {
            "email": "admin@example.com",
            "name": "Admin User",
            "password": generate_password_hash("password_admin"),  # Hashed password
            "role": "Admin",
        },
    ]

    # Mock `load_users` to return test_users
    mocker.patch("models.user.load_users", return_value=test_users)

    # Mock `save_users` to avoid modifying actual data
    mocker.patch("models.user.save_users")


@pytest.fixture
def user_token(app):
    """
    Generate a valid JWT token for a regular user.
    """
    with app.test_request_context():
        return create_access_token(
            identity="user@example.com", additional_claims={"role": "User"}
        )


@pytest.fixture
def admin_token(app):
    """
    Generate a valid JWT token for an admin user.
    """
    with app.test_request_context():
        return create_access_token(
            identity="admin@example.com", additional_claims={"role": "Admin"}
        )


def test_swagger_ui_access(client):
    """
    Test the Swagger UI is accessible.
    """
    response = client.get("/apidocs/")
    assert response.status_code == 200
    # Verify that some consistent text from Swagger UI is present
    assert b"Swagger UI" in response.data or b"swagger-ui" in response.data


def test_register_success(client, setup_test_users):
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


def test_register_duplicate_email(client, setup_test_users):
    """
    Test registration with an already registered email.
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


def test_login_success(client, setup_test_users):
    """
    Test successful login with valid credentials.
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


def test_login_invalid_credentials(client, setup_test_users):
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
