import os
import ast
import uuid


DESTINATION_DATA_FILE = os.path.join(
    os.path.dirname(__file__), "../destination_data.py"
)
BOOKINGS_DATA_FILE = os.path.join(os.path.dirname(__file__), "../bookings_data.py")


def generate_unique_id():
    """
    Generate a unique ID using UUID.
    """
    return str(uuid.uuid4())


def load_destinations():
    """
    Load destinations from the destination_data.py file.
    """
    try:
        with open(DESTINATION_DATA_FILE, "r") as file:
            content = file.read()
            return ast.literal_eval(content.split("=", 1)[1].strip())
    except (FileNotFoundError, SyntaxError, ValueError):
        return []


def save_destinations(destinations):
    """
    Save destinations to the destination_data.py file.
    """
    with open(DESTINATION_DATA_FILE, "w") as file:
        file.write(f"destinations = {destinations}")


def add_destination(destination):
    """
    Add a new destination.
    """
    destinations = load_destinations()
    destination["id"] = generate_unique_id()
    destinations.append(destination)
    save_destinations(destinations)
    return destination


def delete_destination_by_id(destination_id):
    """
    Delete a destination by ID.
    """
    destinations = load_destinations()
    updated_destinations = [d for d in destinations if d["id"] != destination_id]
    if len(destinations) == len(updated_destinations):
        return False  # Not found
    save_destinations(updated_destinations)
    return True  # Success


def load_bookings():
    """
    Load bookings from the bookings_data.py file.
    """
    try:
        with open(BOOKINGS_DATA_FILE, "r") as file:
            content = file.read()
            return ast.literal_eval(content.split("=", 1)[1].strip())
    except (FileNotFoundError, SyntaxError, ValueError):
        return []
