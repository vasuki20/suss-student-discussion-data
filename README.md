# SUSS Student Discussion Data App

This is a simple app with a Flask backend and a React frontend.

## Setup Instructions

### Backend

1.  Navigate to the `backend` directory:

    ```bash
    cd backend
    ```
2.  Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```
3.  Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```
4.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```
5.  Run the Flask app:

    ```bash
    python app.py
    ```

### Frontend

1.  Navigate to the `frontend` directory:

    ```bash
    cd frontend
    ```
2.  Install the dependencies:

    ```bash
    npm install
    ```
3.  Run the React app:

    ```bash
    npm start
    ```

## Dependencies

### Backend

*   Flask
*   Flask-CORS
*   pandas
*   SQLAlchemy
*   openpyxl

### Frontend

*   React
*   react-scripts

## Configuration

*   The backend runs on `http://127.0.0.1:5000`.
*   The frontend runs on `http://localhost:3000`.

## Login Instructions

To log in to the app, find the sample user credentials in the backend logs.
