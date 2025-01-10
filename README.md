# Travel API Microservices Design using Python and Flask

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
│ ├── app.py # Main application entry point for Destination Services
│ ├── controllers/ 
│ ├── views/ 
│ └── tests/ # Unit tests for Destination Services
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
   cd Flask-Python-Assignment
   ```

2. Make sure Python (preferably **3.10+**) is installed on your Linux or Windows machine:
   ```bash
   python3 --version
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

# User Service API
  To start the destination service, run the following command:
  ```bash
  python user-service/app.py
  ```
- The **User Service** will run on:  
  `http://127.0.0.1:5002/apidocs/`

  Navigate to this site to explore and interact with the API endpoints.

---

## **Endpoints**

### **1. POST /register**
**Register a New User**

- To register a new user:
  1. Click on the `/register Register a New User` endpoint.
  2. Click the **`Try it out`** button to enable input fields.
  3. Enter your user details:
     - **`email`**: User's email (must be unique).
     - **`password`**: User's password.
     - **`name`**: Full name of the user.
     - **`role`**: Specify the role (`User` or `Admin`).
  4. Click **`Execute`** to submit the registration request.

- **Recommendations**:
  - It’s suggested to create at least one **Admin** account and one **User** account for testing purposes. Admin accounts are required for accessing restricted endpoints.
  - Validation is implemented: Only one account can be created per email.

- **Data Storage**:
  - User information is stored in the `user-service\user_data.py` file.

---

### **2. POST /login**
**Authenticate a User**

- To log in:
  1. Click on the `/login Authenticate a User` endpoint.
  2. Click the **`Try it out`** button to enable input fields.
  3. Enter the following details:
     - **`email`**: Registered email of the user.
     - **`password`**: Password associated with the account.
  4. Click **`Execute`** to authenticate.

- **Output**:
  - On successful login, a **token** will be generated and displayed in the `Response body`.  
  - **Important**: Copy the token (inside the double quotes) for use in the `/profile` endpoint.

---

### **3. GET /profile**
**Access User Profile Information**

- To access profile details:
  1. **Authorize the Token**:
     - Click on the `Authorize` button (top right corner of the Swagger page).
     - Paste the copied token from the login step in the format:  
       **`Bearer {token}`**  
       Example: `Bearer abcd.1234.efgh`
     - Click **`Authorize`**.
  2. Click on the `/profile Get Profile Information` endpoint.
  3. Click the **`Try it out`** button.
  4. Click **`Execute`** to retrieve the profile.

- **Output**:
  - User profile information will be displayed in the `Response body`. This includes:
    - **Email**
    - **Role**

# Destination Service API
  To start the destination service, run the following command:
   ```bash
   python destination-service/app.py
   ```
  The destination service will be accessible at:  
  `http://127.0.0.1:5001/apidocs/`

  Navigate to this URL to use the available endpoints.

  ---

  ## **Endpoints**

  ### **1. GET /get-destinations**
  **Retrieve a list of all destinations.**

  - Click on the `/get-destinations Retrieve All Destinations` endpoint.
  - Steps:
    1. Click `Try it out`.
    2. Click `Execute` to retrieve all destinations.
  - **Output**: A list of all destinations appears in the `Response body` section.

  ---

  ### **2. POST /add-destination (Admin Specific)**
  **Add a new destination.**

  - Only an admin can access this endpoint. Log in with an admin account using the \login endpoint to generate a bearer token and use the `Authorize` button to authorize as an admin.
  - Click on the `/add-destination Add a New Destination` endpoint.
  - Steps:
    1. Click `Try it out`.
    2. Enter destination details in the provided fields:
      - `name`: Name of the destination.
      - `location`: The location (city, country, etc.) of the destination.
      - `description`: A brief description of the destination.
    3. Click `Execute` to create the destination.
  - **Data Storage**: Destination details are saved in `destination-service\destination_data.py`.
  - **Validation**: 
    - Duplicate destinations cannot be added.
    - Proper data structure is ensured.

  ---

  ### **3. DELETE /delete-destination/{id} (Admin Specific)**
  **Delete a specific destination by its ID.**

  - Only an admin can access this endpoint. Log in with an admin account using the \login endpoint to generate a bearer token and use the `Authorize` button to authorize as an admin.
  - Click on the `/delete-destination/{id} Delete Destination by ID` endpoint.
  - Steps:
    1. Click `Try it out`.
    2. Enter the `ID` of the destination to delete.
    3. Click `Execute`.
  - **Behavior**:
    - If the destination ID exists, the destination is deleted, and a success message is returned.
    - If the destination ID does not exist, an error message is shown.

  ---

  ### **4. GET /get-bookings (Admin Specific)**
  **Retrieve a list of all bookings.**

  - Only an admin can access this endpoint. Log in with an admin account using the \login endpoint to generate a bearer token and use the `Authorize` button to authorize as an admin.
  - Click on the `/get-bookings Retrieve All Bookings` endpoint.
  - Steps:
    1. Click `Try it out`.
    2. Click `Execute` to retrieve all bookings.
  - **Output**: A list of all bookings appears in the `Response body` section.
  - **Data Storage**: Mock booking details are saved in `destination-service\bookings_data.py`.


# Authentication Service API

## **Steps for Using the Authentication Service APIs**
- To start the authentication service, run the following command:
   ```bash
   python auth-service/app.py
   ```
- The **Auth Service** will run on:  
  `http://127.0.0.1:5003/apidocs/`

  Navigate to this site to explore and interact with the API endpoints.

---

### **1. GET /auth-endpoint**
**Admin-Only Access**

- This endpoint is restricted to **Admin users only**.

- To access:
  1. **Authorize the Token**:
     - Click on the `Authorize` button (top right corner of the Swagger page).
     - Enter the **admin token** in the format:  
       **`Bearer {token}`**  
       Example: `Bearer abcd.1234.efgh`
     - Click **`Authorize`**.
  2. Click on the `/auth-endpoint` endpoint.
  3. Click the **`Try it out`** button.
  4. Click **`Execute`** to make the request.

- **Output**:
  - If the token is valid and belongs to an **Admin**, the response will include:  
    **`"message": "Admin access granted. User can add or delete destinations and view the bookings"`**

- **Error Scenarios**:
  - If a non-admin token is used, the response will include:  
    **`"error": "Admin access required"`**
  - If no token or an invalid token is provided, an error message will indicate the issue.

---

## **JWT Error Handling**

- **Unauthorized Access**:
  - If no token is provided:  
    **`"error": "Missing token: Authorization header not provided"`**
  
- **Invalid Token**:
  - If an invalid token is provided:  
    **`"error": "Invalid token"`**

- **Expired Token**:
  - If the token has expired:  
    **`"error": "Token has expired"`**

- **Revoked Token**:
  - If the token has been revoked:  
    **`"error": "Token has been revoked"`**

---

## **Recommendations**

- Always test using both **Admin** and **User** accounts to validate access restrictions.
- Use valid tokens generated during the `/login` process in the **User Service**.
- Tokens are time-sensitive, so ensure they are used before they expire.


## Testing

To ensure that the application works as expected, testing has been set up using **pytest**. Below are the steps and commands to run the tests:

### Running Tests
-  Run all the tests for the **user-service** module:
    ```bash
    pytest user-service
    ```
-  Run all the tests for the **destination-service** module:
    ```bash
    pytest destination-service
    ```
-  Run all the tests for the **authentication-service** module:
    ```bash
    pytest auth-service
    ```

### Checking Test Coverage
-  To check test coverage and get a summary report for the **user-service** module:
    ```bash
    pytest --cov=user-service user-service
    ```
-  To check test coverage and get a summary report for the **destination-service** module:
    ```bash
    pytest --cov=destination-service destination-service
    ```
-  To check test coverage and get a summary report for the **authentication-service** module:
    ```bash
    pytest --cov=auth-service auth-service
    ```

### Viewing Missing Lines in Coverage
To see which lines of code are not covered by your tests, use:
```bash
pytest --cov=user-service --cov-report=term-missing user-service
pytest --cov=destination-service --cov-report=term-missing destination-service
pytest --cov=auth-service --cov-report=term-missing auth-service
```

### Setting Up Tests
Tests are written for the following modules:
- **Models**: Tests functionality related to data handling and operations.
- **Controllers**: Tests business logic and request handling.
- **Views**: Tests API endpoints and ensures they return the correct responses.

Before running tests:
1. Ensure your virtual environment is activated.
2. Install all required dependencies using:
   ```bash
   pip install -r requirements.txt
   ```

