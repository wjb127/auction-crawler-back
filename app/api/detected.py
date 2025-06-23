from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud import detected_item_crud
from app.schemas.detected_item import DetectedItemResponse

router = APIRouter(prefix="/detected", tags=["detected"])


@router.get("", response_model=List[DetectedItemResponse])
async def get_detected_items(
    keyword: Optional[str] = Query(None, description="검색할 키워드"),
    limit: int = Query(50, description="조회할 개수", le=100),
    db: AsyncSession = Depends(get_db)
):
    """감지된 경매 물건 목록 조회"""
    if keyword:
        items = await detected_item_crud.get_by_keyword(db, keyword, limit)
    else:
        items = await detected_item_crud.get_recent_items(db, limit)
    return items


@router.get("/{item_id}", response_model=DetectedItemResponse)
async def get_detected_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """감지된 경매 물건 상세 조회"""
    item = await detected_item_crud.get_by_id(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="경매 물건을 찾을 수 없습니다")
    return item 