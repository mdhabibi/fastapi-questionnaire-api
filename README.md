# FastAPI Questionnaire API

## Overview

This project is a FastAPI application designed to manage and retrieve questionnaire data. It allows users to fetch questions based on specific criteria and add new questions (admin only). The API includes basic authentication for user verification and custom error handling to ensure robustness.

## Problem

In a company that creates questionnaires for smartphone or web browser applications, there is a need to simplify the architecture of different products by setting up an API. This API will query a database to return a series of questions, allowing users to choose a test type and one or more categories, and to specify the number of questions they want. The questions should be returned in random order to allow the generation of multiple MCQs (Multiple Choice Questions) with the same parameters but different questions.

## Solution

This FastAPI application provides endpoints to:
- Retrieve questions based on the test type (`use`), categories (`subjects`), and the number of questions (`num_questions`).
- Verify user credentials with basic authentication.
- Add new questions to the database (admin only).
- Verify that the API is functional.

## Features

- **Retrieve Questions**: Fetch questions based on test type and categories in random order.
- **Add Questions**: Admins can add new questions to the database.
- **Authentication**: Basic authentication for user verification.
- **Error Handling**: Custom error handling and logging for better debugging.
- **API Documentation**: Automatically generated OpenAPI documentation.


## Requirements

- Python 3.7+
- FastAPI
- Pandas
- Uvicorn

## Setup

1. **Clone the repository**:

    ```sh
    git clone https://github.com/mdhabibi/fastapi-questionnaire-api.git
    cd fastapi-questionnaire-api
    ```

2. **Create and activate a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the FastAPI server**:

    ```sh
    uvicorn main:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

- `GET /`: Check API status.
- `GET /questions`: Retrieve questions based on `use`, `subjects`, and `num_questions`.
- `POST /questions`: Add a new question (admin only).
- `GET /my_custom_exception`: Trigger a custom exception for demonstration.

### Example Requests

1. **Check API Status**:

    ```sh
    curl -X GET "http://127.0.0.1:8000/"
    ```

2. **Retrieve Questions**:

    ```sh
    curl -X GET "http://127.0.0.1:8000/questions?use=Test%20de%20positionnement&num_questions=5&subjects=BDD" -u alice:wonderland
    ```

3. **Add a New Question**:

    ```sh
    curl -X POST "http://127.0.0.1:8000/questions" \
    -H "Content-Type: application/json" \
    -d '{
        "question": "What is FastAPI?",
        "subject": "API",
        "use": "Test de positionnement",
        "correct": "A",
        "responseA": "A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.",
        "responseB": "A slow web framework",
        "responseC": "A database",
        "responseD": "A frontend framework",
        "remark": "FastAPI is a modern web framework"
    }' -u admin:4dm1N
    ```

## Testing the API

You can use the provided `test_api.sh` script to test the API. Make sure the server is running, then execute:

```sh
sh test_api.sh
```

## Authentication

The API uses basic authentication. The credentials are as follows:

### Users:

- **alice**: wonderland
- **bob**: builder
- **clementine**: mandarine

### Admin:

- **admin**: 4dm1N

## Conclusion

This FastAPI application serves as a robust backend for managing questionnaire data, providing necessary endpoints for retrieving and adding questions while ensuring secure access through authentication. The project can be further extended with more features such as advanced authentication, real database integration, and more endpoints as required.

