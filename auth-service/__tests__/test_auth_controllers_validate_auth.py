import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from controllers.auth import validate_auth


@pytest.fixture
def app():
    """
    Create a Flask app for testing.
    """
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret-key"
    JWTManager(app)
    return app


def test_validate_auth_admin(mocker, app):
    """
    Test that validate_auth allows admin users.
    """
    with app.test_request_context():
        mocker.patch("controllers.auth.get_jwt", return_value={"role": "Admin"})

        response = validate_auth(identity="test@example.com")
        assert response.status_code == 200
        assert response.get_json() == {"message": "Admin access granted"}


def test_validate_auth_non_admin(mocker, app):
    """
    Test that validate_auth denies non-admin users.
    """
    with app.test_request_context():
        mocker.patch("controllers.auth.get_jwt", return_value={"role": "User"})

        response = validate_auth(identity="test@example.com")
        assert response.status_code == 403
        assert response.get_json() == {"error": "Admin access required"}


def test_validate_auth_missing_role(mocker, app):
    """
    Test that validate_auth denies requests with missing role claims.
    """
    with app.test_request_context():
        # Mock get_jwt to return no role claim
        mocker.patch("controllers.auth.get_jwt", return_value={})

        # Call the function and capture the response
        response = validate_auth(identity="test@example.com")
        assert response.status_code == 403
        assert response.get_json() == {"error": "Admin access required"}
