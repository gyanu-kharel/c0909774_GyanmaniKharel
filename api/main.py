from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from elasticsearch import Elasticsearch, exceptions
from datetime import datetime
import time

app = FastAPI()

es = Elasticsearch("http://elasticsearch:9200")

# Function to log to Elasticsearch
def log_to_elasticsearch(method: str, url: str, body: str, duration: float):
    log_entry = {
        "@timestamp": datetime.now(),
        "method": method,
        "url": url,
        "body": body,
        "duration": duration
    }

    try:
        es.index(index="fastapi-logs", body=log_entry)
    except exceptions.ConnectionError:
        print("Elasticsearch connection error")

# Middleware to log request time and request body
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    body = await request.body()

    response = await call_next(request)

    duration = time.time() - start_time
    log_to_elasticsearch(request.method, str(request.url), body.decode(), duration)

    return response


class TodoModel(BaseModel):
    title: str
    status: str

todos = [{"title": "make coffee", "status": "pending"}, {"title": "Complete assignment", "status": "done"}]



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos")
def create_todo(todo: TodoModel):
    todos.append(todo)

    return JSONResponse(
        content= {'message': 'Created'},
        status_code=201
    )
