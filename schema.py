from pydantic import BaseModel, EmailStr, Field
from enum import Enum 
from typing import Optional

class Status(str,Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskBase(BaseModel):
    description: str
    status: Optional[Status] = "pending"

class TaskInDb(TaskBase):
    user_id: int

class TaskPublic(TaskBase):
    id: int | None = None

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserBase(BaseModel):
    first_name: str 
    last_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str 
    role: Optional[UserRole] = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(UserBase):
    id: int
    password_hash: str
    role: UserRole

class UserPublic(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole

SECRET_KEY = "7834uirh483fu48181yvd788234u1238"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60