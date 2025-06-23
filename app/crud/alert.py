from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.alert import Alert
from app.schemas.alert import AlertCreate


class AlertCRUD:
    async def create(self, db: AsyncSession, alert_in: AlertCreate) -> Alert:
        """알림 생성"""
        alert = Alert(
            user_id=alert_in.user_id,
            item_id=alert_in.item_id,
            message=alert_in.message
        )
        db.add(alert)
        await db.commit()
        await db.refresh(alert)
        return alert
    
    async def get_by_user_id(self, db: AsyncSession, user_id: str, limit: int = 50) -> List[Alert]:
        """사용자별 알림 목록 조회 (관련 물건 정보 포함)"""
        result = await db.execute(
            select(Alert)
            .options(joinedload(Alert.item))
            .where(Alert.user_id == user_id)
            .order_by(Alert.sent_at.desc())
            .limit(limit)
        )
        return result.scalars().unique().all()
    
    async def get_by_id(self, db: AsyncSession, alert_id: int) -> Optional[Alert]:
        """ID로 알림 조회"""
        result = await db.execute(
            select(Alert)
            .options(joinedload(Alert.item))
            .where(Alert.id == alert_id)
        )
        return result.scalar_one_or_none()
    
    async def check_duplicate_alert(self, db: AsyncSession, user_id: str, item_id: int) -> bool:
        """중복 알림 체크"""
        result = await db.execute(
            select(Alert).where(
                (Alert.user_id == user_id) & (Alert.item_id == item_id)
            )
        )
        return result.scalar_one_or_none() is not None
    
    async def get_recent_alerts(self, db: AsyncSession, limit: int = 100) -> List[Alert]:
        """최근 알림 목록 조회"""
        result = await db.execute(
            select(Alert)
            .options(joinedload(Alert.item))
            .order_by(Alert.sent_at.desc())
            .limit(limit)
        )
        return result.scalars().unique().all()


alert_crud = AlertCRUD() 