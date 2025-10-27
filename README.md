# Online Convenience Store

This is a simple e-commerce web application built with Flask.

## Prerequisites

- Python 3.x

## Running the Application Locally

Follow these steps to set up and run the application on your local machine.

### 1. Clone the Repository

First, clone this repository to your local machine if you haven't already.

### 2. Navigate to the Project Directory

Open your terminal or command prompt and navigate to the `Storefront` directory inside the project folder:

```bash
cd path/to/your/project/Storefront
```

### 3. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage the project's dependencies.

**On macOS / Linux:**

```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

**On Windows:**

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

### 4. Run the Application

With the dependencies installed, you can now run the Flask development server:

```bash
flask --app app run
```

Alternatively, you can run the `app.py` file directly:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000/` in your web browser.
