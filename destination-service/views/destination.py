from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from controllers.destination import (
    fetch_all_destinations,
    create_destination,
    remove_destination,
    get_all_bookings,
)

destination_blueprint = Blueprint("destination", __name__)


@destination_blueprint.route("/destinations", methods=["GET"])
def get_destinations():
    """
    Retrieve all destinations
    ---
    responses:
      200:
        description: List of all destinations
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                description: Destination ID
              name:
                type: string
                description: Destination name
              description:
                type: string
                description: Destination description
              location:
                type: string
                description: Destination location
    """
    return jsonify(fetch_all_destinations()), 200


@destination_blueprint.route("/destinations", methods=["POST"])
@jwt_required()
def add_destination():
    """
    Add a new destination (Admins Only)
    ---
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Destination name
              example: Paris
            description:
              type: string
              description: Destination description
              example: City of Lights
            location:
              type: string
              description: Destination location
              example: France
    responses:
      201:
        description: Destination added successfully
      400:
        description: Invalid input
      401:
        description: Unauthorized or not an admin
    """
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return jsonify({"error": "Access denied. Admins only."}), 401

    try:
        data = request.get_json()
        destination = create_destination(data)
        return (
            jsonify(
                {
                    "message": "Destination added successfully",
                    "destination": destination,
                }
            ),
            201,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@destination_blueprint.route(
    "/destinations/<string:destination_id>", methods=["DELETE"]
)
@jwt_required()
def delete_destination(destination_id):
    """
    Delete a destination (Admins Only)
    ---
    security:
      - Bearer: []
    parameters:
      - name: destination_id
        in: path
        required: true
        type: string
        description: ID of the destination to delete
    responses:
      200:
        description: Destination deleted successfully
      401:
        description: Unauthorized or not an admin
      404:
        description: Destination not found
    """
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return jsonify({"error": "Access denied. Admins only."}), 401

    try:
        remove_destination(destination_id)
        return jsonify({"message": "Destination deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@destination_blueprint.route("/bookings", methods=["GET"])
@jwt_required()
def view_all_bookings():
    """
    View all bookings (Admins Only)
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: List of all bookings
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: Booking ID
              user_email:
                type: string
                description: Email of the user who made the booking
              booking_date_time:
                type: string
                format: date-time
                description: Booking date and time
              departure_time:
                type: string
                format: date-time
                description: Scheduled departure time
              arrival_time:
                type: string
                format: date-time
                description: Scheduled arrival time
              destination:
                type: string
                description: Booking destination
              stay_duration_days:
                type: integer
                description: Duration of stay in days
      401:
        description: Unauthorized access
      403:
        description: Forbidden - Admin access required
    """
    # Check admin role
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return jsonify({"error": "Access denied. Admins only."}), 403

    # Fetch all bookings
    bookings = get_all_bookings()
    return jsonify(bookings), 200
