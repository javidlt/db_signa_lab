from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class User(BaseModel):
    uid: str | None
    username: str
    email: str
    created_at: datetime | None