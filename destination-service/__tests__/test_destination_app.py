import pytest
from flask import Flask
from unittest.mock import patch
from flask_jwt_extended import JWTManager, create_access_token
from views.destination import destination_blueprint


@pytest.fixture
def app():
    """
    Create a Flask app for testing.
    """
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "shared-secret-key"
    JWTManager(app)  # Initialize JWTManager
    app.register_blueprint(destination_blueprint)
    return app


@pytest.fixture
def client(app):
    """
    Create a test client for the app.
    """
    return app.test_client()


@pytest.fixture
def admin_token(app):
    """
    Generate a valid JWT token for an admin.
    """
    with app.test_request_context():
        return create_access_token(identity="admin@example.com", additional_claims={"role": "Admin"})


@pytest.fixture
def user_token(app):
    """
    Generate a valid JWT token for a regular user.
    """
    with app.test_request_context():
        return create_access_token(identity="user@example.com", additional_claims={"role": "User"})


@patch("views.destination.fetch_all_destinations")
def test_get_destinations(mock_fetch, client):
    """
    Test retrieving all destinations.
    """
    # Define mock destinations to return
    mock_destinations = [
        {"id": "1", "name": "Paris", "description": "City of Lights", "location": "France"},
        {"id": "2", "name": "New York", "description": "Big Apple", "location": "USA"},
    ]
    # Mock the controller function
    mock_fetch.return_value = mock_destinations

    # Make a GET request to the /destinations endpoint
    response = client.get("/destinations")

    # Assert the response
    assert response.status_code == 200
    assert response.get_json() == mock_destinations
    mock_fetch.assert_called_once()  # Ensure the mock was called




@patch("views.destination.create_destination")
def test_add_destination_success(mock_create, client, admin_token):
    """
    Test adding a destination as admin.
    """
    # Mock the return value of create_destination
    mock_create.return_value = {
        "id": "3",
        "name": "Tokyo",
        "description": "Land of the Rising Sun",
        "location": "Japan",
    }

    # Data to be sent in the POST request
    data = {"name": "Tokyo", "description": "Land of the Rising Sun", "location": "Japan"}

    # Make a POST request to add a destination
    response = client.post(
        "/destinations",
        json=data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    # Assert the response
    assert response.status_code == 201
    assert response.get_json()["message"] == "Destination added successfully"
    assert response.get_json()["destination"]["name"] == "Tokyo"

    # Ensure the mock was called with the correct arguments
    mock_create.assert_called_once_with(data)



def test_add_destination_unauthorized(client, user_token):
    """
    Test adding a destination as a regular user (unauthorized).
    """
    data = {"name": "Tokyo", "description": "Land of the Rising Sun", "location": "Japan"}
    response = client.post(
        "/destinations",
        json=data,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Access denied. Admins only."


@patch("views.destination.remove_destination")
def test_delete_destination_success(mock_remove, client, admin_token):
    """
    Test deleting a destination as admin.
    """
    # Mock the return value to indicate successful deletion
    mock_remove.return_value = None

    # Make a DELETE request to delete the destination
    response = client.delete(
        "/destinations/1", headers={"Authorization": f"Bearer {admin_token}"}
    )

    # Assert the response
    assert response.status_code == 200
    assert response.get_json()["message"] == "Destination deleted successfully"

    # Ensure the mock was called with the correct ID
    mock_remove.assert_called_once_with("1")



def test_delete_destination_unauthorized(client, user_token):
    """
    Test deleting a destination as a regular user (unauthorized).
    """
    response = client.delete(
        "/destinations/1", headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Access denied. Admins only."


@patch("controllers.destination.get_all_bookings")
def test_view_all_bookings_success(mock_get_bookings, client, admin_token):
    """
    Test viewing all bookings as admin.
    """
    # Updated mock data to match the actual structure
    mock_bookings = [
        {
            "id": 1,
            "user_email": "john.doe@example.com",
            "destination": "Paris",
            "booking_date_time": "2024-11-21T12:30:00",
            "departure_time": "2024-12-01T08:00:00",
            "arrival_time": "2024-12-01T12:30:00",
            "stay_duration_days": 5,
        },
        {
            "id": 2,
            "user_email": "jane.smith@example.com",
            "destination": "New York",
            "booking_date_time": "2024-11-22T15:00:00",
            "departure_time": "2024-12-05T10:00:00",
            "arrival_time": "2024-12-05T14:30:00",
            "stay_duration_days": 7,
        },
    ]

    # Mock the `get_all_bookings` function to return the mock data
    mock_get_bookings.return_value = mock_bookings

    # Make the GET request to the `/bookings` endpoint
    response = client.get("/bookings", headers={"Authorization": f"Bearer {admin_token}"})

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response matches the mock data
    assert response.get_json() == mock_bookings

    # Ensure the mock function was called once
    mock_get_bookings.assert_called_once()



def test_view_all_bookings_unauthorized(client, user_token):
    """
    Test viewing all bookings as a regular user (unauthorized).
    """
    response = client.get("/bookings", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 403
    assert response.get_json()["error"] == "Access denied. Admins only."
