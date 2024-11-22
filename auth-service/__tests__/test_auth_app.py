import pytest  # type: ignore
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from views.auth import auth_blueprint
from flasgger import Swagger


@pytest.fixture
def app():
    """
    Create a Flask app for testing.
    """
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "shared-secret-key"
    JWTManager(app)
    app.register_blueprint(auth_blueprint)

    # Initialize Swagger for testing
    Swagger(
        app,
        template={
            "swagger": "2.0",
            "info": {
                "title": "Auth Service API",
                "description": "API that demonstrates admin-only access using JWT.",
                "version": "1.0.0",
            },
            "host": "127.0.0.1:5003",
            "basePath": "/",
            "schemes": ["http"],
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'",
                }
            },
            "security": [{"Bearer": []}],
        },
    )
    return app


@pytest.fixture
def client(app):
    """
    Create a test client for the Flask app.
    """
    return app.test_client()


@pytest.fixture
def admin_token(app):
    """
    Generate a valid admin JWT token.
    """
    with app.test_request_context():
        token = create_access_token(
            identity="admin@example.com",  # Set identity to a string
            additional_claims={"role": "Admin"}  # Add role as a custom claim
        )
        print("Generated Admin Token:", token)
    return token


@pytest.fixture
def user_token(app):
    """
    Generate a valid user JWT token.
    """
    with app.test_request_context():
        token = create_access_token(
            identity="user@example.com",  # Set identity to a string
            additional_claims={"role": "User"}  # Add role as a custom claim
        )
        print("Generated User Token:", token)
    return token


def test_swagger_ui_access(client):
    """
    Test that the Swagger UI is accessible.
    """
    response = client.get("/apidocs/")
    assert response.status_code == 200
    assert b"swagger-ui" in response.data  # Class name used in the Swagger UI


def test_auth_endpoint_admin_access(client, admin_token):
    """
    Test that the /auth-endpoint allows access for admin users.
    """
    response = client.get(
        "/auth-endpoint",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Admin access granted"
    }


def test_auth_endpoint_non_admin_access(client, user_token):
    """
    Test that the /auth-endpoint denies access for non-admin users.
    """
    response = client.get(
        "/auth-endpoint",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 403
    assert response.get_json() == {"error": "Admin access required"}


def test_auth_endpoint_no_token(client):
    """
    Test that the /auth-endpoint denies access when no token is provided.
    """
    response = client.get("/auth-endpoint")
    assert response.status_code == 401
    assert response.get_json().get("msg") == "Missing Authorization Header"


def test_auth_endpoint_invalid_token(client):
    """
    Test that the /auth-endpoint denies access for invalid tokens.
    """
    invalid_token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYWtlIn0.invalidsignature"
    )
    response = client.get(
        "/auth-endpoint",
        headers={"Authorization": f"Bearer {invalid_token}"},
    )
    assert response.status_code == 422
    assert response.get_json().get("msg") == "Signature verification failed"
