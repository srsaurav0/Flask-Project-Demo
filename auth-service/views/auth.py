from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from controllers.auth import validate_auth

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route('/auth-endpoint', methods=['GET'])
@jwt_required()
def auth_endpoint():
    """
    Admin-Only Endpoint
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: Admin access granted.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Success message
              example: Admin access granted
      403:
        description: Forbidden - Admin access required
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
              example: Admin access required
    """
    identity = get_jwt_identity()
    claims = get_jwt()  # Retrieve additional claims
    print(f"Extracted Identity: {identity}")  # Log identity
    print(f"JWT Claims: {claims}")  # Log claims

    validation_error = validate_auth(identity)
    if validation_error:
        print(f"Validation Error: {validation_error}")  # Debugging log
        return validation_error

    return jsonify({"message": "Admin access granted. User can add or delete destinations and view the bookings"}), 200
