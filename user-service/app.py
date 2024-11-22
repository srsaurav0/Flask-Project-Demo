from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from views.user import user_blueprint

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "shared-secret-key"
swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "User Service API",
            "description": "API for user registration, authentication, and profile management",
            "version": "1.0.0",
        },
        "host": "127.0.0.1:5002",
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

# Register blueprints
app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    app.run(port=5002)
