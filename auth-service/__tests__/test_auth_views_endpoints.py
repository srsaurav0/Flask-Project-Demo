import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from flasgger import Swagger  # Import Swagger for proper initialization
from views.auth import auth_blueprint


@pytest.fixture
def app():
    """
    Create a Flask app for testing.
    """
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "shared-secret-key"
    JWTManager(app)

    # Initialize Flasgger for Swagger UI
    Swagger(
        app,
        template={
            "swagger": "2.0",
            "info": {
                "title": "Auth Service API",
                "description": "API that demonstrates admin-only access using JWT.",
                "version": "1.0.0",
            },
            "host": "127.0.0.1:5000",
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

    app.register_blueprint(auth_blueprint)
    return app


@pytest.fixture
def admin_token(app):
    """
    Generate a valid admin JWT token.
    """
    with app.test_request_context():
        token = create_access_token(
            identity="admin@example.com",  # Set identity to a string
            additional_claims={"role": "Admin"},  # Add role as a custom claim
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
            additional_claims={"role": "User"},  # Add role as a custom claim
        )
        print("Generated User Token:", token)
    return token


def test_auth_endpoint_admin(client, admin_token):
    """
    Test that the /auth-endpoint allows access for admin users.
    """
    response = client.get(
        "/auth-endpoint",
        headers={
            "Authorization": f"Bearer {admin_token}",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {"message": "Admin access granted"}


def test_auth_endpoint_non_admin(client, user_token):
    """
    Test that the /auth-endpoint denies access for non-admin users.
    """
    response = client.get(
        "/auth-endpoint",
        headers={
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json",
        },
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
