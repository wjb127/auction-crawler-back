from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from app.models.detected_item import DetectedItem
from app.schemas.detected_item import DetectedItemCreate


class DetectedItemCRUD:
    async def create(self, db: AsyncSession, item_in: DetectedItemCreate) -> DetectedItem:
        """감지된 물건 생성"""
        item = DetectedItem(
            title=item_in.title,
            appraisal_value=item_in.appraisal_value,
            bid_date=item_in.bid_date,
            url=item_in.url,
            keywords=item_in.keywords,
            source_site=item_in.source_site
        )
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item
    
    async def get_by_id(self, db: AsyncSession, item_id: int) -> Optional[DetectedItem]:
        """ID로 물건 조회"""
        result = await db.execute(
            select(DetectedItem).where(DetectedItem.id == item_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_url(self, db: AsyncSession, url: str) -> Optional[DetectedItem]:
        """URL로 물건 조회 (중복 체크용)"""
        result = await db.execute(
            select(DetectedItem).where(DetectedItem.url == url)
        )
        return result.scalar_one_or_none()
    
    async def get_recent_items(self, db: AsyncSession, limit: int = 50) -> List[DetectedItem]:
        """최근 감지된 물건 목록 조회"""
        result = await db.execute(
            select(DetectedItem)
            .order_by(DetectedItem.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_keyword(self, db: AsyncSession, keyword: str, limit: int = 50) -> List[DetectedItem]:
        """키워드로 물건 검색"""
        result = await db.execute(
            select(DetectedItem)
            .where(
                or_(
                    DetectedItem.title.ilike(f"%{keyword}%"),
                    DetectedItem.keywords.op("@>")(f'["{keyword}"]')
                )
            )
            .order_by(DetectedItem.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_matching_items(self, db: AsyncSession, keywords: List[str], limit: int = 100) -> List[DetectedItem]:
        """여러 키워드와 매칭되는 물건 조회"""
        conditions = []
        for keyword in keywords:
            conditions.append(DetectedItem.title.ilike(f"%{keyword}%"))
            conditions.append(DetectedItem.keywords.op("@>")(f'["{keyword}"]'))
        
        result = await db.execute(
            select(DetectedItem)
            .where(or_(*conditions))
            .order_by(DetectedItem.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()


detected_item_crud = DetectedItemCRUD() 