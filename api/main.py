from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()


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


@app.get("/test")
def test():
    return JSONResponse(
        content={'message': 'test passed'},
        status_code=200
    )
