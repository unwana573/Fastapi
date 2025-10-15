from fastapi import FastAPI, Query, Path, status, HTTPException
from schema import TaskInDb, TaskPublic
from typing import List


app = FastAPI(title="Todo App")

tasks = {}

@app.post("/add-task", response_model=TaskPublic, status_code=status.HTTP_200_OK)
def add_task(task:TaskInDb):
    if task.user_id not in tasks:
        tasks[task.user_id] = [{'task':task.task, 'status':task.status}]
    else:
        tasks[task.user_id].append({'task':task.task, 'status':task.status})
    return TaskPublic(task=task.task, status=task.status)


@app.get("/task/{user_id}", response_model=List[TaskPublic])
def view_task(user_id:int = Path(description="User id in format ")):
    all_tasks = []
    if user_id not in tasks:
        raise HTTPException(status_code=404, detail="User id not found")
    users_tasks = tasks[user_id]
    for task in users_tasks:
        t = TaskPublic(task=task['task'], status=task['status'])
        all_tasks.append(t)
    return all_tasks




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

# Additional tasks
# - Filter by certain dates