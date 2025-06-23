from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud import alert_crud
from app.schemas.alert import AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=List[AlertResponse])
async def get_alerts(
    user_id: str = Query(..., description="사용자 ID"),
    limit: int = Query(50, description="조회할 개수", le=100),
    db: AsyncSession = Depends(get_db)
):
    """사용자별 알림 기록 조회"""
    alerts = await alert_crud.get_by_user_id(db, user_id, limit)
    return alerts


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db)
):
    """알림 상세 조회"""
    alert = await alert_crud.get_by_id(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="알림을 찾을 수 없습니다")
    return alert 