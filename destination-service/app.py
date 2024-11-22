from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from views.destination import destination_blueprint

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "shared-secret-key"
swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "Destination Service API",
            "description": "API for managing travel destinations with secure access",
            "version": "1.0.0",
        },
        "host": "127.0.0.1:5001",
        "basePath": "/",
        "schemes": ["http"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"',
            }
        },
        "security": [{"Bearer": []}],  # Apply Bearer authentication globally
    },
)
jwt = JWTManager(app)

# Register the blueprint
app.register_blueprint(destination_blueprint)

if __name__ == "__main__":
    app.run(port=5001)
