import pytest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from unittest.mock import patch
from views.destination import destination_blueprint


@pytest.fixture
def app():
    """
    Create a Flask app for testing.
    """
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret-key"
    JWTManager(app)
    app.register_blueprint(destination_blueprint)
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


@patch("views.destination.fetch_all_destinations")  # Ensure the correct import path
def test_get_destinations(mock_fetch, client):
    """
    Test retrieving all destinations.
    """
    mock_destinations = [
        {
            "id": "1",
            "name": "Paris",
            "description": "City of Lights",
            "location": "France",
        },
        {"id": "2", "name": "New York", "description": "Big Apple", "location": "USA"},
    ]
    mock_fetch.return_value = mock_destinations

    response = client.get("/destinations")
    assert response.status_code == 200

    # Use sorted comparison if IDs or ordering differ
    response_data = response.get_json()
    assert sorted(response_data, key=lambda x: x["id"]) == sorted(
        mock_destinations, key=lambda x: x["id"]
    )
    mock_fetch.assert_called_once()


@patch("views.destination.create_destination")  # Ensure the correct path is patched
def test_add_destination_success(mock_create, client, admin_token):
    """
    Test adding a destination as admin.
    """
    mock_create.return_value = {
        "id": "3",
        "name": "Tokyo",
        "description": "Land of the Rising Sun",
        "location": "Japan",
    }
    data = {
        "name": "Tokyo",
        "description": "Land of the Rising Sun",
        "location": "Japan",
    }
    response = client.post(
        "/destinations",
        json=data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    # Assertions for response
    assert response.status_code == 201
    assert response.get_json()["message"] == "Destination added successfully"
    assert response.get_json()["destination"]["name"] == "Tokyo"

    # Assertion for mocked function
    mock_create.assert_called_once_with(data)


def test_add_destination_unauthorized(client, user_token):
    """
    Test adding a destination as a non-admin user.
    """
    data = {
        "name": "Tokyo",
        "description": "Land of the Rising Sun",
        "location": "Japan",
    }
    response = client.post(
        "/destinations",
        json=data,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Access denied. Admins only."


@patch("views.destination.remove_destination")  # Ensure the correct path is patched
def test_delete_destination_success(mock_remove, client, admin_token):
    """
    Test deleting a destination as admin.
    """
    # Mock the remove_destination function to simulate successful deletion
    mock_remove.return_value = True

    response = client.delete(
        "/destinations/1", headers={"Authorization": f"Bearer {admin_token}"}
    )

    # Assertions
    assert response.status_code == 200
    assert response.get_json()["message"] == "Destination deleted successfully"

    # Verify the mock was called with the correct destination ID
    mock_remove.assert_called_once_with("1")


def test_delete_destination_unauthorized(client, user_token):
    """
    Test deleting a destination as a non-admin user.
    """
    response = client.delete(
        "/destinations/1", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Access denied. Admins only."


@patch("views.destination.get_all_bookings")
def test_view_all_bookings_success(mock_get_bookings, client, admin_token):
    """
    Test viewing all bookings as admin.
    """
    # Mock data aligned with actual bookings structure
    mock_bookings = [
        {
            "id": 1,
            "user_email": "john.doe@example.com",
            "booking_date_time": "2024-11-21T12:30:00",
            "departure_time": "2024-12-01T08:00:00",
            "arrival_time": "2024-12-01T12:30:00",
            "destination": "Paris",
            "stay_duration_days": 5,
        },
        {
            "id": 2,
            "user_email": "jane.smith@example.com",
            "booking_date_time": "2024-11-22T15:00:00",
            "departure_time": "2024-12-05T10:00:00",
            "arrival_time": "2024-12-05T14:30:00",
            "destination": "New York",
            "stay_duration_days": 7,
        },
    ]

    # Mock the function to return the updated mock_bookings
    mock_get_bookings.return_value = mock_bookings

    # Make the GET request
    response = client.get(
        "/bookings", headers={"Authorization": f"Bearer {admin_token}"}
    )

    # Assertions
    assert response.status_code == 200
    assert response.get_json() == mock_bookings  # Ensure the response matches the mock
    mock_get_bookings.assert_called_once()  # Verify the mock was called


def test_view_all_bookings_unauthorized(client, user_token):
    """
    Test viewing all bookings as a non-admin user.
    """
    response = client.get(
        "/bookings", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
    assert response.get_json()["error"] == "Access denied. Admins only."


def test_view_all_bookings_no_token(client):
    """
    Test viewing all bookings without a token.
    """
    response = client.get("/bookings")
    assert response.status_code == 401
    assert response.get_json()["msg"] == "Missing Authorization Header"
