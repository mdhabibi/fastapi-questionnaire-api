#!/bin/bash

# Test API status
curl -X GET "http://127.0.0.1:8000/"

# Test getting questions
curl -X GET "http://127.0.0.1:8000/questions?use=Test%20de%20positionnement&num_questions=5&subjects=BDD" -u alice:wonderland

# Test adding a question
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
