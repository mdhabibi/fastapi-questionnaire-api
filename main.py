import logging
from fastapi import FastAPI, HTTPException, Depends, status, Request, Query
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the dataset
try:
    df = pd.read_csv('questions.csv')
    logger.info("CSV file loaded successfully")
except Exception as e:
    logger.error(f"Error loading CSV file: {e}")
    raise

# Initialize FastAPI
app = FastAPI(
    title="Questionnaire API",
    description="API to query a database to return a series of questions.",
    version="1.0.0"
)

# Security
security = HTTPBasic()

# User credentials
users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

admin_password = "4dm1N"

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_password = users.get(credentials.username)
    if correct_password is None or correct_password != credentials.password:
        logger.error(f"Authentication failed for user: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    logger.info(f"User {credentials.username} authenticated successfully")
    return credentials.username

def is_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != admin_password:
        logger.error(f"Admin authentication failed for user: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    logger.info("Admin authenticated successfully")
    return credentials.username

@app.get("/", tags=["home"], summary="Check API status")
async def read_root():
    return {"message": "API is working"}

@app.get("/questions", tags=["questions"], summary="Get questions")
async def get_questions(
    use: str,
    num_questions: int,
    subjects: List[str] = Query(...),
    username: str = Depends(get_current_username)
):
    logger.info(f"Received request for questions with use: {use}, num_questions: {num_questions}, subjects: {subjects}")

    if num_questions not in [5, 10, 20]:
        logger.error(f"Invalid number of questions: {num_questions}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of questions must be 5, 10, or 20"
        )
    
    try:
        filtered_df = df[(df['use'] == use) & (df['subject'].isin(subjects))]
        logger.info(f"Filtered dataframe: {filtered_df}")
    except Exception as e:
        logger.error(f"Error filtering dataframe: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    if len(filtered_df) < num_questions:
        logger.error("Not enough questions available")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not enough questions available"
        )

    try:
        questions = filtered_df.sample(num_questions).to_dict(orient='records')
        questions = [{k: (v if pd.notna(v) else None) for k, v in q.items()} for q in questions]
        logger.info(f"Sampled questions: {questions}")
    except Exception as e:
        logger.error(f"Error sampling questions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    return {"questions": questions}

class Question(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: Optional[str] = None
    responseD: Optional[str] = None
    remark: Optional[str] = None

@app.post("/questions", tags=["admin"], summary="Add a new question")
async def add_question(
    question: Question,
    username: str = Depends(is_admin)
):
    new_question = question.dict()
    global df
    try:
        df = pd.concat([df, pd.DataFrame([new_question])], ignore_index=True)
        logger.info(f"Question added: {new_question}")
    except Exception as e:
        logger.error(f"Error adding question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    return {"message": "Question added successfully"}

# Custom exception class
class MyException(Exception):
    def __init__(self, name: str, date: str):
        self.name = name
        self.date = date

# Custom exception handler
@app.exception_handler(MyException)
def my_exception_handler(request: Request, exception: MyException):
    logger.error(f"MyException occurred: {exception}")
    return JSONResponse(
        status_code=418,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': 'This error is my own',
            'date': exception.date
        }
    )

@app.get('/my_custom_exception', tags=["errors"], summary="Trigger a custom exception")
def get_my_custom_exception():
    raise MyException(
        name='my error',
        date=str(pd.Timestamp.now())
    )

# Document possible errors
responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}

@app.get('/thing', responses=responses, tags=["errors"], summary="Get thing with possible errors")
def get_thing():
    return {'data': 'hello world'}

# Run the server
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000, reload=True)
