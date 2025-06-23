from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.keyword import Keyword
from app.schemas.keyword import KeywordCreate, KeywordUpdate


class KeywordCRUD:
    async def create(self, db: AsyncSession, keyword_in: KeywordCreate) -> Keyword:
        """키워드 생성"""
        keyword = Keyword(
            user_id=keyword_in.user_id,
            keyword=keyword_in.keyword
        )
        db.add(keyword)
        await db.commit()
        await db.refresh(keyword)
        return keyword
    
    async def get_by_user_id(self, db: AsyncSession, user_id: str) -> List[Keyword]:
        """사용자별 키워드 목록 조회"""
        result = await db.execute(
            select(Keyword).where(Keyword.user_id == user_id).order_by(Keyword.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_by_id(self, db: AsyncSession, keyword_id: int) -> Optional[Keyword]:
        """ID로 키워드 조회"""
        result = await db.execute(
            select(Keyword).where(Keyword.id == keyword_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all_keywords(self, db: AsyncSession) -> List[str]:
        """모든 키워드 목록 조회 (중복 제거)"""
        result = await db.execute(
            select(Keyword.keyword).distinct()
        )
        return [keyword for keyword in result.scalars().all()]
    
    async def update(self, db: AsyncSession, keyword_id: int, keyword_update: KeywordUpdate) -> Optional[Keyword]:
        """키워드 수정"""
        keyword = await self.get_by_id(db, keyword_id)
        if not keyword:
            return None
        
        for field, value in keyword_update.dict(exclude_unset=True).items():
            setattr(keyword, field, value)
        
        await db.commit()
        await db.refresh(keyword)
        return keyword
    
    async def delete(self, db: AsyncSession, keyword_id: int) -> bool:
        """키워드 삭제"""
        result = await db.execute(
            delete(Keyword).where(Keyword.id == keyword_id)
        )
        await db.commit()
        return result.rowcount > 0


keyword_crud = KeywordCRUD() 