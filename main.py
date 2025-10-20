from fastapi import FastAPI, Query, Path, status, HTTPException, Depends
from schema import TaskPublic, TaskInDb
from typing import List, Optional
import  uuid
from task import app
from database import get_db, Database
from schema import Status
from queries import *


tasks:dict = {}

@app.post("/add-task", response_model=TaskPublic) # @app - a decorator  
async def add_task(task:TaskInDb, db:Database = Depends(get_db)):
    add_task_query
    task_id = str(uuid.uuid4())  # generate a unique task ID
    print(f" New Task ID: {task_id}")
    task_data = {'tasks': task.task, 'status': task.status.value, 'user_id': task.user_id}
    await db.execute(query=add_task_query, values=task_data)    
    return TaskPublic(task = task.task, status=task.status)   


@app.get("/view-task/{user_id}", response_model=List[TaskPublic])
async def view_task(db:Database = Depends(get_db)):
    result = await db.fetch_all(select_data_from_customers_query)
    data_result = []
    for data in result:
        data_result.append(TaskPublic(task=data['tasks'], status=Status.PENDING, 
            id=str(data['user_id'])))
        
    return data_result


@app.put("/update-task/{task_id}")
async def update_user_tasks(
    task_id: int = Path(description="Task ID"),
    task: str = Query(description="New Task"),
    db:Database = Depends(get_db)):

    task_data = {'id': task_id, 'tasks' : task}

    await db.execute(query=update_task, values=task_data)


@app.delete("/delete-task/{task_id}")
async def delete_user_task(task_id: str = Path(description="Task ID"), db: Database = Depends(get_db)):
    task_data = {"id": task_id}
    await db.execute(query=delete_task_query, values=task_data)
    return {"message": f"Task {task_id} deleted successfully ✅"}
# @app.delete("/delete-task/{task_id}")
# async def delete_task(task_id: str = Path(description="Task ID"), db:Database = Depends(get_db)):
#     task_data = {'id' : task_id}

#     await db.execute(query=delete_task_query, values=(task_data))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)