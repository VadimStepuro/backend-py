from fastapi import FastAPI
from dotenv import load_dotenv

# Initialize FastAPI app
app = FastAPI()
load_dotenv()

# Define a route
@app.get("/api/v1")
def read_root():
    return {"message": "Hello, FastAPI"}

# Additional routes can be defined similarly
