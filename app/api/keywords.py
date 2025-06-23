from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crud import keyword_crud
from app.schemas.keyword import KeywordCreate, KeywordResponse

router = APIRouter(prefix="/keywords", tags=["keywords"])


@router.get("", response_model=List[KeywordResponse])
async def get_keywords(
    user_id: str = Query(..., description="사용자 ID"),
    db: AsyncSession = Depends(get_db)
):
    """사용자의 키워드 목록 조회"""
    keywords = await keyword_crud.get_by_user_id(db, user_id)
    return keywords


@router.post("", response_model=KeywordResponse, status_code=201)
async def create_keyword(
    keyword_in: KeywordCreate,
    db: AsyncSession = Depends(get_db)
):
    """새 키워드 등록"""
    keyword = await keyword_crud.create(db, keyword_in)
    return keyword


@router.delete("/{keyword_id}", status_code=204)
async def delete_keyword(
    keyword_id: int,
    db: AsyncSession = Depends(get_db)
):
    """키워드 삭제"""
    success = await keyword_crud.delete(db, keyword_id)
    if not success:
        raise HTTPException(status_code=404, detail="키워드를 찾을 수 없습니다")
    return None


@router.get("/{keyword_id}", response_model=KeywordResponse)
async def get_keyword(
    keyword_id: int,
    db: AsyncSession = Depends(get_db)
):
    """키워드 상세 조회"""
    keyword = await keyword_crud.get_by_id(db, keyword_id)
    if not keyword:
        raise HTTPException(status_code=404, detail="키워드를 찾을 수 없습니다")
    return keyword 