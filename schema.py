from pydantic import BaseModel
from enum import Enum 
from typing import Optional

class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class TaskBase(BaseModel):
    task: str
    status: Optional[Status] = Status.PENDING

class TaskInDb(TaskBase):
    user_id: int

class TaskPublic(TaskBase):
    id: str | None = None
