from pydantic import BaseModel, EmailStr, Field
from enum import Enum 
from typing import Optional, List

class Status(str,Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskBase(BaseModel):
    description: str
    status: Optional[Status] = "pending"

class TaskInDb(TaskBase):
    pass

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

class UserPublicList(BaseModel):
    data: List[UserPublic]
    count: int

class TokenData(BaseModel):
    id: int
    email: str
    role: str