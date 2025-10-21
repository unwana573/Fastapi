from pydantic import BaseModel, EmailStr
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


class UserCreate(BaseModel):
    email: EmailStr

