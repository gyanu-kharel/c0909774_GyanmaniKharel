from fastapi import FastAPI

app = FastAPI()


todos = [{"title": "make coffee", "status": "pending"}, {"title": "Complete assignment", "status": "done"}]



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/todos")
def get_todos():
    return todos