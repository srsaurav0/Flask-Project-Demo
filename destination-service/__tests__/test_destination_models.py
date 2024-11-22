import pytest
from unittest.mock import patch
from models.destination import (
    load_destinations,
    save_destinations,
    add_destination,
    delete_destination_by_id,
    load_bookings,
    generate_unique_id,
)


@pytest.fixture
def mock_destinations():
    """
    Provide mock destinations data.
    """
    return [
        {"id": "1234", "name": "Paris", "country": "France"},
        {"id": "5678", "name": "New York", "country": "USA"},
    ]


@pytest.fixture
def mock_bookings():
    """
    Provide mock bookings data.
    """
    return [
        {"id": "abcd", "destination_id": "1234", "user_id": "user1"},
        {"id": "efgh", "destination_id": "5678", "user_id": "user2"},
    ]


@patch("models.destination.load_destinations")
@patch("models.destination.save_destinations")
def test_add_destination(mock_save, mock_load, mock_destinations):
    """
    Test adding a new destination.
    """
    mock_load.return_value = mock_destinations
    new_destination = {"name": "Tokyo", "country": "Japan"}

    added_destination = add_destination(new_destination)

    assert added_destination["id"] is not None
    assert added_destination["name"] == "Tokyo"
    assert added_destination["country"] == "Japan"
    mock_save.assert_called_once()


@patch("models.destination.load_destinations")
@patch("models.destination.save_destinations")
def test_delete_destination_by_id(mock_save, mock_load, mock_destinations):
    """
    Test deleting a destination by ID.
    """
    mock_load.return_value = mock_destinations

    result = delete_destination_by_id("1234")  # ID to delete
    assert result is True

    # Ensure save_destinations was called with updated data
    updated_destinations = [
        {"id": "5678", "name": "New York", "country": "USA"}
    ]
    mock_save.assert_called_once_with(updated_destinations)

    # Test deleting a non-existent ID
    result = delete_destination_by_id("non-existent-id")
    assert result is False


@patch("models.destination.load_bookings")  # Update with correct path
def test_load_bookings(mock_load):
    """
    Test loading bookings.
    """
    mock_bookings = [
        {"id": "abcd", "destination_id": "1234", "user_id": "user1"},
        {"id": "efgh", "destination_id": "5678", "user_id": "user2"},
    ]
    mock_load.return_value = mock_bookings  # Mock return value

    bookings = load_bookings()  # Call the function under test

    assert len(bookings) == 2  # Assert the mocked response is used
    assert bookings[0]["destination_id"] == "1234"
    assert bookings[1]["destination_id"] == "5678"


@patch("models.destination.generate_unique_id")
def test_generate_unique_id(mock_generate):
    """
    Test unique ID generation.
    """
    mock_generate.return_value = "mocked-uuid"
    unique_id = generate_unique_id()
    assert unique_id == "mocked-uuid"
