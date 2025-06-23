from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List


class DetectedItemBase(BaseModel):
    title: str
    appraisal_value: Optional[int] = None
    bid_date: Optional[date] = None
    url: str
    keywords: Optional[List[str]] = None
    source_site: Optional[str] = None


class DetectedItemCreate(DetectedItemBase):
    pass


class DetectedItemResponse(DetectedItemBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True 