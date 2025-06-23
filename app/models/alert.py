from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("detected_items.id"), nullable=False)
    message = Column(Text)
    sent_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # 관계 설정
    item = relationship("DetectedItem", backref="alerts")
    
    def __repr__(self):
        return f"<Alert(id={self.id}, user_id='{self.user_id}', item_id={self.item_id})>" 