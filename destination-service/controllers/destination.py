from models.destination import (
    load_destinations,
    add_destination,
    delete_destination_by_id,
    load_bookings,
)


def fetch_all_destinations():
    """
    Controller to fetch all destinations.
    """
    return load_destinations()


def create_destination(data):
    """
    Controller to validate and create a new destination.
    """
    required_fields = ["name"]
    if any(field not in data for field in required_fields):
        raise ValueError("Missing required fields")

    new_destination = {
        "name": data["name"],
        "description": data.get("description", ""),
        "location": data.get("location", ""),
    }

    return add_destination(new_destination)


def remove_destination(destination_id):
    """
    Controller to handle destination deletion.
    """
    if not delete_destination_by_id(destination_id):
        raise ValueError("Destination not found")


def get_all_bookings():
    """
    Fetch all bookings from the data source.
    """
    return load_bookings()
