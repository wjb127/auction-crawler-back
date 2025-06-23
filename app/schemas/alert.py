from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .detected_item import DetectedItemResponse


class AlertBase(BaseModel):
    user_id: str
    item_id: int
    message: Optional[str] = None


class AlertCreate(AlertBase):
    pass


class AlertResponse(AlertBase):
    id: int
    sent_at: datetime
    item: Optional[DetectedItemResponse] = None
    
    class Config:
        from_attributes = True 