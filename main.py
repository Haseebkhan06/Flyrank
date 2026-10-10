

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": True},
    {"id": 2, "title": "Build my first API", "done": False},
    {"id": 3, "title": "Test API endpoints", "done": False}
]


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{id}")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

   
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

@app.post("/tasks", status_code=201)
async def create_task(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body must be valid JSON"}
        )

    title = data.get("title") if isinstance(data, dict) else None

    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required and cannot be empty"}
        )

    next_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": next_id,
        "title": title.strip(),
        "done": False
    }

    tasks.append(new_task)
    return new_task

from fastapi import Request
from fastapi.responses import JSONResponse, Response


@app.put("/tasks/{id}")
async def update_task(id: int, request: Request):
    # Find the task
    task = next((t for t in tasks if t["id"] == id), None)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    # Read the JSON body
    try:
        data = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid JSON body"}
        )

    # Validate the body
    if not isinstance(data, dict) or not data:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    if not set(data).issubset({"title", "done"}):
        return JSONResponse(
            status_code=400,
            content={"error": "Only title and done can be updated"}
        )

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

    if "done" in data and not isinstance(data["done"], bool):
        return JSONResponse(
            status_code=400,
            content={"error": "Done must be true or false"}
        )

    # Apply the changes
    if "title" in data:
        task["title"] = data["title"].strip()

    if "done" in data:
        task["done"] = data["done"]

    return task


@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):
    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

