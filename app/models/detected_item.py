from sqlalchemy import Column, Integer, String, Text, BigInteger, Date, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base


class DetectedItem(Base):
    __tablename__ = "detected_items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    appraisal_value = Column(BigInteger)
    bid_date = Column(Date)
    url = Column(Text, nullable=False)
    keywords = Column(JSON)  # ["송파구", "아파트"] 형태
    source_site = Column(String(100))  # 크롤링 출처
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<DetectedItem(id={self.id}, title='{self.title[:50]}...', bid_date='{self.bid_date}')>" 