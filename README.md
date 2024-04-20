````markdown
# Flask Student Assignment Management

Welcome to the Flask Student Assignment Management app! This application provides a platform for managing student assignments with authentication functionality.

## Overview

This Flask application offers the following features:

- Authentication: Users can log in to access the assignment management functionalities.
- Assignment Management: Users can perform CRUD operations (Create, Read, Update, Delete) on student assignments.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flask-assignment-management.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Ensure you have SQLite installed.
   - Run the following command to create the necessary database tables:
     ```bash
     python db.py
     ```

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Access the application:
   - Open your web browser and navigate to `http://localhost:5000`.
   - Log in using your credentials to access the assignment management dashboard.

## API Endpoints

### Authentication

- **URL**: `/login`
  - **Method**: POST
  - **Request Body**:
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - **Response**:
    ```json
    {
      "token": "your_jwt_token"
    }
    ```

### Assignment Management

- **GET All Assignments**
  - **URL**: `/assignments`
  - **Method**: GET

- **Create New Assignment**
  - **URL**: `/assignments`
  - **Method**: POST
  - **Request Body**:
    ```json
    {
      "name": "Assignment Name",
      "description": "Assignment Description",
      "due_date": "YYYY-MM-DD"
    }
    ```

- **Update Assignment**
  - **URL**: `/assignments/{assignment_id}`
  - **Method**: PUT
  - **Request Body**:
    ```json
    {
      "name": "Updated Assignment Name",
      "description": "Updated Assignment Description",
      "due_date": "YYYY-MM-DD"
    }
    ```

- **Delete Assignment**
  - **URL**: `/assignments/{assignment_id}`
  - **Method**: DELETE


