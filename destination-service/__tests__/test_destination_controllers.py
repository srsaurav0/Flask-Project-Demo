import pytest
from unittest.mock import patch
from controllers.destination import (
    fetch_all_destinations,
    create_destination,
    remove_destination,
    get_all_bookings,
)


@pytest.fixture
def mock_destinations():
    """
    Provide mock destinations data.
    """
    return [
        {
            "id": "1",
            "name": "Paris",
            "description": "City of Lights",
            "location": "France",
        },
        {"id": "2", "name": "New York", "description": "Big Apple", "location": "USA"},
    ]


@pytest.fixture
def mock_bookings():
    """
    Provide mock bookings data.
    """
    return [
        {"id": "101", "destination_id": "1", "user_id": "user1"},
        {"id": "102", "destination_id": "2", "user_id": "user2"},
    ]


@patch("controllers.destination.load_destinations")
def test_fetch_all_destinations(mock_load_destinations, mock_destinations):
    """
    Test fetch_all_destinations controller.
    """
    mock_load_destinations.return_value = mock_destinations

    destinations = fetch_all_destinations()

    assert len(destinations) == len(mock_destinations)
    assert destinations == mock_destinations
    mock_load_destinations.assert_called_once()


@patch("controllers.destination.add_destination")
def test_create_destination_success(mock_add_destination):
    """
    Test create_destination controller for successful creation.
    """
    mock_add_destination.return_value = {
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

    new_destination = create_destination(data)

    assert new_destination["name"] == "Tokyo"
    assert new_destination["description"] == "Land of the Rising Sun"
    assert new_destination["location"] == "Japan"

    mock_add_destination.assert_called_once_with(
        {
            "name": "Tokyo",
            "description": "Land of the Rising Sun",
            "location": "Japan",
        }
    )


def test_create_destination_missing_fields():
    """
    Test create_destination controller with missing required fields.
    """
    data = {"description": "Missing name field"}
    with pytest.raises(ValueError, match="Missing required fields"):
        create_destination(data)


@patch(
    "controllers.destination.delete_destination_by_id"
)
def test_remove_destination_success(mock_delete_destination):
    """
    Test remove_destination controller for successful deletion.
    """
    mock_delete_destination.return_value = True

    try:
        remove_destination("1")
    except ValueError:
        pytest.fail("remove_destination raised ValueError unexpectedly")

    mock_delete_destination.assert_called_once_with("1")


@patch(
    "controllers.destination.delete_destination_by_id"
)
def test_remove_destination_failure(mock_delete_destination):
    """
    Test remove_destination controller for failure case.
    """
    mock_delete_destination.return_value = False

    with pytest.raises(ValueError, match="Destination not found"):
        remove_destination("non-existent-id")

    mock_delete_destination.assert_called_once_with("non-existent-id")


@patch("models.destination.delete_destination_by_id")
def test_remove_destination_not_found(mock_delete_destination):
    """
    Test remove_destination controller when destination is not found.
    """
    mock_delete_destination.return_value = False

    with pytest.raises(ValueError, match="Destination not found"):
        remove_destination("non-existent-id")


@patch("controllers.destination.load_bookings")
def test_get_all_bookings(mock_load_bookings):
    """
    Test get_all_bookings controller.
    """
    mock_bookings = [
        {"id": "101", "destination_id": "1", "user_id": "user1"},
        {"id": "102", "destination_id": "2", "user_id": "user2"},
    ]

    mock_load_bookings.return_value = mock_bookings

    bookings = get_all_bookings()

    assert len(bookings) == 2
    assert bookings == mock_bookings
    mock_load_bookings.assert_called_once()
