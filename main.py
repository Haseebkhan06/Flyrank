

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()


tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": True},
    {"id": 2, "title": "Build my first API", "done": False},
    {"id": 3, "title": "Test API endpoints", "done": False}
]


@app.get("/", summary="Root Endpoint", description="Returns basic information about the API.")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health", summary ="Health Check", description="Returns the health status of the API.")
def health():
    return {"status": "ok"}

@app.get(
    "/tasks",
    summary="List all tasks",
    description="Returns every task currently stored in memory."
)
def get_tasks():
    return tasks

@app.get("/tasks/{id}", summary="Get a specific task", description="Returns the task with the specified ID.")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

   
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

class TaskCreate(BaseModel):
    title: str
    
@app.post(
    "/tasks",
    status_code=201,
    summary="Create a new task",
    description="Creates a new task with the provided title."
)
def create_task(data: TaskCreate):
    title = data.title.strip()

    if not title:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    next_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": next_id,
        "title": title,
        "done": False
    }

    tasks.append(new_task)
    return new_task



