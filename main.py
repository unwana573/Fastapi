from fastapi import FastAPI, Query, Path, status, HTTPException, Depends
from schema import TaskPublic, TaskInDb, UserLogin, UserCreate, UserPublic, UserPublicList, TokenData
from typing import List, Optional
import uuid
from task import app
from database import get_db, Database
from queries import *
import asyncpg
from sql.create_sql_table import *
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from config import *

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/login")
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

pwd_context = PasswordHash.recommended()

def hash_password(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def verify_access_token_validity(token:str, db:Database):
    value = await db.execute(query=get_token_query, values={'token':token})
    # if value:
    return value

async def get_current_user(token:str = Depends(oauth2scheme), db: Database = Depends(get_db)):
    try:
        # access_token = token['access_token']
        token_check = await verify_access_token_validity(token, db)
        if token_check:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = token
        data = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
        email = data['sub']
        existing_user = await db.fetch_one(query=check_email_query, values={"email": email})
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return UserPublic(**existing_user)
    except ExpiredSignatureError:
        raise  HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"})

async def require_admin(current_user: TokenData = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only!",
        )
    return current_user

# @app.get("/users/me")
# async def get_user(token:str, db:Database = Depends(get_db)):
#     user = await get_current_user(token=token, db=db)
#     return user

@app.get("/users/me")
async def get_user(current_user:UserPublic = Depends(get_current_user)):
    return current_user

@app.post('/register', response_model=UserPublic)
async def register_user(user: UserCreate, 
                        db:Database = Depends(get_db),
                        ):
    existing_user = await db.fetch_one(query=check_email_query, values={"email": user.email})
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email already registered")
    
    password = hash_password(user.password)
    
    new_user = await db.fetch_one(
        query=insert_user_query,
        values={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": password,
            "role": user.role.value,
        },
    )
    return new_user

@app.post('/login', response_model=dict)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db:Database = Depends(get_db)):
    user = await db.fetch_one(query=check_email_query, values={"email": form_data.username})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user["email"], "role": user["role"]})

    # await db.execute(query=update_token_query, values={"token": access_token, "id": user["id"]})

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout")
async def logout_user(
    db: Database = Depends(get_db),
    token: str = Depends(oauth2scheme),
    current_user: UserPublic = Depends(get_current_user)
):
    await db.execute(query=blacklist_token_query, values={"token": token})
    return {"message": "Logout successful"}

@app.get("/users", response_model=UserPublicList)
async def get_all_users(db: Database = Depends(get_db),
                        current_user: TokenData = Depends(require_admin)):
    users = await db.fetch_all(query=get_all_users_query)
    user_list = [dict(user) for user in users]  
    return {
        "data": user_list,
        "count": len(user_list)
    }

@app.post("/add-task", response_model=TaskPublic)
async def add_task(task: TaskInDb, db:Database = Depends(get_db), 
                    current_user: UserPublic = Depends(get_current_user),):
    add_task_query
    values = {
    # "id": task.user_id,    
    "user_id": current_user.id,
    "description": task.description,
    "status": task.status.value
    }
    try:
        new_task = await db.fetch_one(query=add_task_query, values=values)
        add_task = TaskPublic(
            description = new_task["description"],
            status = new_task["status"],
            id = new_task["id"]
    )   
        return add_task 
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="User already exists")

@app.get("/users/{user_id}/tasks", response_model=List[TaskPublic])
async def view_task(db:Database = Depends(get_db), 
                    current_user: UserPublic = Depends(get_current_user)):
    query = select_data_from_users_query
    result = await db.fetch_all(query)
    data_result = []
    for data in result:
        data_result.append(TaskPublic(description=data['description'], status=data["status"], 
            id=data['id']))
        
    return data_result

@app.put("/users/{user_id}/tasks/{task_id}")
async def update_user_tasks(
    updated_task: TaskInDb,
    user_id: int = Path(description="User ID"),
    task_id: int = Path(description="Task ID"),
    current_user: UserPublic = Depends(get_current_user),
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

@app.delete("/users/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: int = Path(description="User ID"), 
    task_id: int = Path(description="Task ID"), 
    current_user: UserPublic = Depends(get_current_user),
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

