# Travel API Implementation using Python and Flask

This project is a modular **Travel API** built using Flask, following the **Model-View-Controller (MVC)** architecture. It includes authentication, user management, and destination services.

---

## Features

- **User Service**:
  - Register users with roles (Admin/User).
  - Login functionality with JWT-based authentication.
  - Fetch user profile.

- **Auth Service**:
  - Admin-only access for specific actions.
  - Token validation.

- **Destination Service**:
  - Manage destinations (CRUD operations).

---

## Tech Stack

- **Backend**: Flask
- **Authentication**: Flask-JWT-Extended
- **Documentation**: Flasgger (Swagger)
- **Testing**: Pytest

---

## Directory Structure

``` CSS
FLASK-PYTHON-ASSIGNMENT/ 
├── auth-service/ 
│ ├── app.py # Main application entry point for Auth Service 
│ ├── controllers/ 
│ ├── views/ 
│ └── tests/ # Unit tests for Auth Service 
├── user-service/ 
│ ├── app.py # Main application entry point for User Service 
│ ├── controllers/ 
│ ├── models/ 
│ ├── views/ 
│ └── tests/ # Unit tests for User Service 
├── destination-service/ 
│ ├── app.py # Main application entry point for Destination Service 
│ ├── controllers/ 
│ ├── views/ 
│ └── tests/ # Unit tests for Destination Service 
├── .gitignore 
└── README.md 
└── requirements.txt
```