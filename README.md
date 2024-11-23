# Travel API Implementation using Python and Flask

This project is a modular **Travel API** built using Flask, following the **Model-View-Controller (MVC)** architecture. It includes authentication, user management, and destination services.

---

## Features

- **User Service**:
  - Register users with roles (Admin/User).
  - Login functionality with JWT-based authentication.
  - Fetch user profile.

- **Destination Service**:
  - Add new destination (Admin-only)
  - View all destination
  - Delete destination by id (Admin-only)
  - View all bookings (Admin-only)

- **Auth Service**:
  - Recognizing admin by token.

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
├── README.md 
└── requirements.txt
```

## Prerequisites

- Python 3.8+
- Virtual Environment (optional but recommended)

---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/srsaurav0/Flask-Python-Assignment.git
   cd travel-api-mvc
   ```

2. Make sure Python (preferably **3.10+**) is installed on your Windows machine:
   ```bash
   python --version
   ```
   If Python is not installed, download it from **python.org** and install it. Ensure you check the box **Add Python to PATH** during installation.

3. Set Up a Virtual Environment:
- For Linux:
  - Create a virtual environment:
    ```bash
    python3 -m venv .venv
    ```
  - Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```
  If successful, your terminal prompt will change to include `(.venv)`.

- For Windows:
  - Create a virtual environment:
    ```bash
    python -m venv .venv
    ```
  - Change Execution Policy Temporarily:
    ```bash
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ```
  - .\venv\Scripts\activate:
    ```bash
    .\venv\Scripts\activate
    ```
  If successful, your terminal prompt will change to include `(.venv)`.

4. Install **project dependencies** inside `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

5. Environment Setup:
   Set Environment Variables:
   ```bash
   set FLASK_APP=app.py
   set FLASK_ENV=development
   ```
6. Run the App:
  - Run **User Service**:
   ```bash
   python user-service/app.py
   ```
  The user service will run on `http://127.0.0.1:5001/apidocs/`. Navigate to this site to use the 3 endpoints.
  Steps of using the User Service APIs:
    - **POST /register**
      - At first create an user. Click on the */register Register a New User* to create an user.
      - Click on the `Try it out` button to enter your details and then the `Execute` button to complete the registration.
      - You can define the `role` of an user during the registration process. It can be either an `user` or an `admin` It is recommended to create an `user` account and an `admin` account. The admin account can be used later for access to some **restricted endpoints**.
      - The user information is stored inside *user-service\user_data.py* file.
      - Validation is properly implemented in this section. Only one account can be created with a single email.
    - **POST /login**
      - Click on the */login Authenticate a User* to log in.
      - Click on the `Try it out` button to enter your details and then the `Execute` button to complete loggin in.
      - After successful log in, a `token` will be generated inside the `Response body` section. **Copy** the token (Inside the double quotation)
      - This `token` is mandatory to access the **/profile** endpoint
    - **GET ​/profile**
      - Click on the `Authorize` button on the *top right corner* of the page. The bearer token is needed to be entered here. Inside the `value` field, enter the key copied after the **log in** process using in format `Bearer {key}` (Example: Bearer abcd.1234.__.alsdf)
      - Click on the */profile Get Profile Information* to access the user information.
      - Click on the `Try it out` button to enter your details and then the `Execute` button to complete loggin in.
      - After successful log in, a `token` will be generated inside the `Response body` section. **Copy** the token (Inside the double quotation)
      - This `token` is mandatory to access the **/profile** endpoint