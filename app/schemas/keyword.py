from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class KeywordBase(BaseModel):
    user_id: str
    keyword: str


class KeywordCreate(KeywordBase):
    pass


class KeywordUpdate(BaseModel):
    keyword: Optional[str] = None


class KeywordResponse(KeywordBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True 