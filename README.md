# Service Record Management System

This is a full-stack web application for managing service records. It features a responsive frontend built with HTML, Tailwind CSS, and vanilla JavaScript, and a robust backend API powered by Flask and connected to a PostgreSQL database.

The application provides a clean and intuitive interface for performing all essential CRUD (Create, Read, Update, Delete) operations on service records.

***

## 🚀 Features

* **Full CRUD Functionality**: Create, read, update, and delete service records seamlessly.
* **Dynamic Filtering**: Filter records instantly by date, service adviser, or vehicle model.
* **Modal-based Forms**: A clean user experience for adding and editing records without leaving the page.
* **RESTful API Backend**: A well-structured Flask API to handle all business logic and data persistence.
* **Decoupled Architecture**: A static frontend that communicates with a separate backend API, allowing for independent development and scaling.

***

## 🛠️ Tech Stack

* **Backend**: Python, Flask, PostgreSQL, psycopg2
* **Frontend**: HTML, Tailwind CSS, Vanilla JavaScript
* **Server**: Gunicorn (for production, optional)

***

## 📂 Project Structure

```
├── app.py                # The main Flask API application
├── templates
  └── index.html          # The static frontend file
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (for database URL)
```

***

## ⚙️ Setup and Installation

Follow these steps to get the application running locally.

### Prerequisites

* **Python 3.8+**
* **PostgreSQL** installed and running.
* A tool to interact with your database (e.g., `psql`, DBeaver, PgAdmin).

### 1. Backend Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Amankalyankar/Car_maintenance.git
    cd Car_maintenance
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Create `requirements.txt`**:
    Create a file named `requirements.txt` and add the following dependencies:
    ```
    Flask
    Flask-Cors
    psycopg2-binary
    python-dotenv
    ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up the PostgreSQL Database**:
    * Connect to your PostgreSQL instance and create a new database.
        ```sql
        CREATE DATABASE service_records_db;
        ```
    * Connect to your new database and run the following SQL command to create the necessary table:
        ```sql
        CREATE TABLE service_records (
            sr_no SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            adviser VARCHAR(255) NOT NULL,
            model VARCHAR(255) NOT NULL,
            reg_no VARCHAR(50) NOT NULL,
            amount NUMERIC(10, 2) NOT NULL,
            discount NUMERIC(10, 2) DEFAULT 0.00
        );
        ```

6.  **Configure Environment Variables**:
    * Create a file named `.env` in the root of your project.
    * Add your database connection URL to it. **Replace the placeholder values with your actual database credentials.**
        ```
        # Example: postgresql://<user>:<password>@<host>:<port>/<database_name>
        DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5432/service_records_db"
        ```

7.  **Run the Flask Server**:
    ```bash
    flask run
    ```
    The backend API will now be running at `http://127.0.0.1:5000`.

### 2. Frontend Setup

The frontend is a single static file (`index.html`). You just need to open it in a web browser.

* **Open `index.html`**: Simply double-click the `index.html` file to open it in your default web browser.

The JavaScript code is written to communicate with the Flask API running at `http://127.0.0.1:5000`. As long as the backend is running, the frontend will work correctly.

***

## 🔌 API Endpoints

The Flask backend provides the following RESTful API endpoints:

| Method | Endpoint                    | Description                                         |
| :----- | :-------------------------- | :-------------------------------------------------- |
| `GET`  | `/api/records`              | Fetches all records. Can be filtered with query params (`date`, `adviser`, `model`). |
| `POST` | `/api/records`              | Creates a new service record.                       |
| `PUT`  | `/api/records/<record_id>`  | Updates an existing record by its ID.               |
| `DELETE`| `/api/records/<record_id>`  | Deletes a specific record by its ID.                |
