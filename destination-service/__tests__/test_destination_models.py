import pytest
from unittest.mock import patch
from models.destination import (
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
@patch("models.destination.generate_unique_id")
def test_add_destination(mock_generate_id, mock_save, mock_load, mock_destinations):
    """
    Test adding a new destination.
    """
    mock_load.return_value = mock_destinations
    mock_generate_id.return_value = "mocked-id"
    new_destination = {"name": "Tokyo", "country": "Japan"}

    added_destination = add_destination(new_destination)

    expected_destinations = [
        {"id": "1234", "name": "Paris", "country": "France"},
        {"id": "5678", "name": "New York", "country": "USA"},
        {"id": "mocked-id", "name": "Tokyo", "country": "Japan"},
    ]

    assert added_destination == {"id": "mocked-id", "name": "Tokyo", "country": "Japan"}
    mock_save.assert_called_once_with(expected_destinations)
    mock_generate_id.assert_called_once()


@patch("models.destination.load_destinations")
@patch("models.destination.save_destinations")
def test_delete_destination_by_id(mock_save, mock_load, mock_destinations):
    """
    Test deleting a destination by ID.
    """
    mock_load.return_value = mock_destinations

    result = delete_destination_by_id("1234")
    assert result is True

    updated_destinations = [{"id": "5678", "name": "New York", "country": "USA"}]
    mock_save.assert_called_once_with(updated_destinations)

    result = delete_destination_by_id("non-existent-id")
    assert result is False


@patch("test_destination_models.load_bookings")
def test_load_bookings(mock_load):
    """
    Test loading bookings.
    """

    mock_bookings = [
        {"id": "abcd", "destination_id": "1234", "user_id": "user1"},
        {"id": "efgh", "destination_id": "5678", "user_id": "user2"},
    ]

    mock_load.return_value = mock_bookings

    bookings = load_bookings()

    print("Mock called:", mock_load.called)
    print("Mock call count:", mock_load.call_count)
    print("Bookings returned:", bookings)

    assert len(bookings) == 2
    assert bookings == mock_bookings
    mock_load.assert_called_once()


@patch("controllers.destination.generate_unique_id")
def test_generate_unique_id(mock_generate):
    """
    Test unique ID generation.
    """
    mock_generate.return_value = "mocked-uuid"

    print("Mock setup complete")

    unique_id = generate_unique_id()

    print("Mock called:", mock_generate.call_count)

    assert unique_id == "mocked-uuid"
    mock_generate.assert_called_once()
