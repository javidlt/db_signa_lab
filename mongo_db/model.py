from pydantic import BaseModel
from typing import Optional

class TweetsModel(BaseModel):
    id: Optional[str]
    user: str
    content: str
    timestamp: Optional[str]