from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from controllers.user import register_user, authenticate_user, fetch_profile


user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/register", methods=["POST"])
def register():
    """
    Register a New User
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User's email
              example: user@example.com
            password:
              type: string
              description: User's password
              example: password123
            name:
              type: string
              description: User's full name
              example: John Doe
            role:
              type: string
              description: User's role (User or Admin)
              example: User
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input or email already registered
    """
    try:
        data = request.get_json()
        user = register_user(data)
        return jsonify({"message": "User registered successfully", "user": user}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_blueprint.route("/login", methods=["POST"])
def login():
    """
    Authenticate a User
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: User's email
              example: user@example.com
            password:
              type: string
              description: User's password
              example: password123
    responses:
      200:
        description: Login successful
      400:
        description: Missing email or password
      401:
        description: Invalid credentials
    """
    try:
        data = request.get_json()
        user = authenticate_user(data)
        token = create_access_token(identity=user["email"], additional_claims={"role": user["role"]})
        return jsonify({"token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_blueprint.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """
    Get Profile Information
    ---
    security:
      - Bearer: []
    responses:
      200:
        description: User's profile details
        schema:
          type: object
          properties:
            email:
              type: string
              description: User's email
            role:
              type: string
              description: User's role
      401:
        description: Unauthorized
    """
    current_user = get_jwt_identity()
    claims = get_jwt()
    return jsonify(fetch_profile(current_user)), 200
