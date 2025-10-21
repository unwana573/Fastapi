from fastapi import FastAPI, Query, Path, status, HTTPException, Depends
from schema import TaskPublic, TaskInDb, UserLogin, UserCreate, UserPublic
from typing import List, Optional
import uuid
from task import app
from database import get_db, Database
from schema import Status
from queries import *
import asyncpg
from sql.create_sql_table import *
from passlib.context import CryptContext

#register user
# 1. ask for user details (firstname, lastname, email, password, role)
# 2. check if user already exists
# 3. if user does not exist, create the user in the database.
# 4. if user exists, return error message that email already exists

#login
# 1. give user details (email, password)
# 2. verify the user details
# 3. if user details are correct, return a token. 
# 

#accessing protected endpoints
# 1. The frontend sends this token in every request they make to the backend.
# 2. The backend verifies the token. 
# 3. If the token is valid, we allow access to the endpoint , otherwise we return an unauthorised error message

pwd_context = CryptContext(schemes=['bcrypt'], deprecated=['auto'])

def hash_password(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password )

@app.post('/register', response_model=UserPublic)
async def register_user(user: UserCreate, 
                        db:Database = Depends(get_db),
                        ):
    existing_user = await db.fetch_one(query=check_email_query, values={"email": user.email})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    password = hash_password(user.password)
    
    new_user = await db.fetch_one(
        query=insert_user_query,
        values={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": password,
            "role": user.role,
        },
    )

    return new_user


@app.post('/login', response_model=UserPublic)
async def login_user(user: UserLogin):
    pass

@app.post("/add-task", response_model=TaskPublic)
async def add_task(task: TaskInDb, db:Database = Depends(get_db)):
    add_task_query
    values = {
    # "id": task.user_id,    
    "id": task.user_id,
    "description": task.description,
    "status": task.status.value
    }
    try:
        new_task = await db.fetch_one(query=add_task_query, values=values)
        print(new_task)
        add_task = TaskPublic(
            description = new_task["description"],
            status = new_task["status"],
            id = new_task["id"]
    )   
        return add_task 
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="User already exists")

@app.get("/view-task/{user_id}", response_model=List[TaskPublic])
async def view_task(db:Database = Depends(get_db)):
    query = select_data_from_users_query
    result = await db.fetch_all(query)
    data_result = []
    for data in result:
        data_result.append(TaskPublic(description=data['description'], status=data["status"], 
            id=data['id']))
        
    return data_result

@app.put("/update-task/{user_id}/{task_id}")
async def update_user_tasks(
    updated_task: TaskInDb,
    user_id: int = Path(description="User ID"),
    task_id: int = Path(description="Task ID"),
    db:Database = Depends(get_db)):

    select_user_query
    existing_task = await db.fetch_one(query=select_user_query, values={"id": task_id, "user_id": user_id})
    if not select_user_query:
        raise HTTPException(status_code=404, detail="User id not found")

    update_query
    values = {
        "description": updated_task.description,
        "status": updated_task.status.value,
        "id": task_id,
        "user_id": user_id, 
    }
    updated_row = await db.fetch_one(query=update_query, values=values)
    return {
        "message": "Task updated successfully ✅",
        "task": updated_row
    }
    # raise HTTPException(status_code=404, detail="Task id not found")

@app.delete("/delete-task/{user_id}/{task_id}")
async def delete_task(
    user_id: int = Path(description="User ID"), 
    task_id: int = Path(description="Task ID"), 
    db:Database = Depends(get_db)):
    try:
        # Execute delete query
        delete_query
        rows_affected = await db.execute(query=delete_query, values={"id": task_id, "user_id": user_id})

        # ✅ Check if any row was deleted
        if rows_affected == 0:
            raise HTTPException(status_code=404, detail="Task not found")

        return {"message": f"Task {task_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

