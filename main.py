from fastapi import FastAPI, Query, Path, status, HTTPException
from schema import TaskPublic, TaskInDb
from typing import List
import  uuid

app = FastAPI(title="Todo App")

tasks = {}

@app.post("/add-task") # @app - a decorator  
def add_task(task:TaskInDb, response_model=TaskPublic):
    task_id = str(uuid.uuid4())  # generate a unique task ID
    print(f" New Task ID: {task_id}")
    task_data = {'id': task_id, 'task': task.task, 'status': task.status}
    if task.user_id not in tasks:
        tasks[task.user_id] = [task_data]
    else:
        tasks[task.user_id].append(task_data)    
    return TaskPublic(task=task.task, status=task.status)   


@app.get("/view-task/{user_id}", response_model=List[TaskPublic])
def view_task(user_id: int = Path(description="User id in format")):
    all_task = [] 
    user_tasks = tasks[user_id]
    for task in user_tasks: 
        t = TaskPublic(id=task['id'], task=task['task'], status=task['status'])
        all_task.append(t)
    return all_task  

@app.put("/update-task/{user_id}/{task_id}")
def update_user_tasks(
    user_id: int = Path(description="User ID"),
    task_id: str = Path(description="Task ID"),
    updated_task: TaskInDb = None):

    if user_id not in tasks:
        raise HTTPException(status_code=404, detail="User id not found")

    for task in tasks[user_id]:
        if task["id"] == task_id:
            task["task"] = updated_task.task
            task["status"] = updated_task.status
            return {"message": "Task updated successfully", "task": task}

    raise HTTPException(status_code=404, detail="Task id not found")

@app.delete("/delete-task/{user_id}/{task_id}")
def delete_task(user_id: int = Path(description="User ID"), task_id: str = Path(description="Task ID")):
    if user_id not in tasks:
        raise HTTPException(status_code=404, detail="User id not found")

    user_tasks = tasks[user_id]
    updated_tasks = [task for task in user_tasks if task["id"] != task_id]

    if len(updated_tasks) == len(user_tasks):
        raise HTTPException(status_code=404, detail="Task id not found")

    tasks[user_id] = updated_tasks
    return {"message": f"Task {task_id} deleted successfully", "remaining_tasks": tasks[user_id]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)