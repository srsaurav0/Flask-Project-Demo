from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from views.auth import auth_blueprint

app = Flask(__name__)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "shared-secret-key"
jwt = JWTManager(app)


# JWT Error Handlers
@jwt.unauthorized_loader
def unauthorized_callback(err):
    """
    Handles missing JWT in the Authorization header.
    """
    return jsonify({"error": f"Missing token: {err}"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(err):
    """
    Handles invalid JWT tokens.
    """
    return jsonify({"error": f"Invalid token: {err}"}), 422


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """
    Handles expired JWT tokens.
    """
    return jsonify({"error": "Token has expired"}), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """
    Handles revoked JWT tokens.
    """
    return jsonify({"error": "Token has been revoked"}), 401


# Swagger Configuration
swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "Auth Service API",
            "description": "API that demonstrates admin-only access using JWT.",
            "version": "1.0.0",
        },
        "host": "127.0.0.1:5003",
        "basePath": "/",
        "schemes": ["http"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'",
            }
        },
        "security": [{"Bearer": []}],
    }
)

# Register the auth blueprint
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(port=5003)
