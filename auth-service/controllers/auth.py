from flask import jsonify, make_response
from flask_jwt_extended import get_jwt


def validate_auth(identity):
    """
    Validates if the user has admin privileges.
    """
    claims = get_jwt()  # Retrieve additional claims from the JWT
    print(f"JWT Claims: {claims}")  # Debugging log
    if claims.get("role") != "Admin":
        return make_response(jsonify({"error": "Admin access required"}), 403)
    return make_response(jsonify({"message": "Admin access granted"}), 200)
