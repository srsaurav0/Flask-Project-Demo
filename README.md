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

# User Service API
  To start the destination service, run the following command:
  ```bash
  python user-service/app.py
  ```
- The **User Service** will run on:  
  `http://127.0.0.1:5001/apidocs/`

  Navigate to this site to explore and interact with the API endpoints.

---

## **Steps for Using the User Service APIs**

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
  `http://127.0.0.1:5002/apidocs/`

  Navigate to this URL to use the available endpoints.

  ---

  ## **Endpoints**

  ### **1. POST /add-destination**
  **Add a new destination.**

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

  ### **2. GET /get-destinations**
  **Retrieve a list of all destinations.**

  - Click on the `/get-destinations Retrieve All Destinations` endpoint.
  - Steps:
    1. Click `Try it out`.
    2. Click `Execute` to retrieve all destinations.
  - **Output**: A list of all destinations appears in the `Response body` section.

  ---

  ### **3. DELETE /delete-destination/{id}**
  **Delete a specific destination by its ID.**

  - Click on the `/delete-destination/{id} Delete Destination by ID` endpoint.
  - Steps:
    1. Click `Try it out`.
    2. Enter the `ID` of the destination to delete.
    3. Click `Execute`.
  - **Behavior**:
    - If the destination ID exists, the destination is deleted, and a success message is returned.
    - If the destination ID does not exist, an error message is shown.

  ---

  ### **4. POST /book-destination**
  **Book a destination.**

  - Click on the `/book-destination Book a Destination` endpoint.
  - Steps:
    1. Click `Try it out`.
    2. Enter booking details:
      - `destination_id`: The ID of the destination to book (retrieve from `/get-destinations`).
      - `user_id`: The ID of the user making the booking.
      - `arrival_time`: Arrival date and time (ISO 8601 format).
      - `departure_time`: Departure date and time (ISO 8601 format).
    3. Click `Execute` to create the booking.
  - **Data Storage**: Booking details are saved in `destination-service\bookings_data.py`.

  ---

  ### **5. GET /get-bookings**
  **Retrieve a list of all bookings.**

  - Click on the `/get-bookings Retrieve All Bookings` endpoint.
  - Steps:
    1. Click `Try it out`.
    2. Click `Execute` to retrieve all bookings.
  - **Output**: A list of all bookings appears in the `Response body` section.