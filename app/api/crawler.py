from typing import Dict
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.crawler import CourtAuctionCrawler
from app.services import KeywordMatcher

router = APIRouter(prefix="/crawler", tags=["crawler"])


@router.post("/run", response_model=Dict)
async def run_crawler(
    background_tasks: BackgroundTasks,
    pages: int = 3,
    db: AsyncSession = Depends(get_db)
):
    """수동 크롤링 실행"""
    
    # 백그라운드에서 크롤링 실행
    background_tasks.add_task(perform_crawling, db, pages)
    
    return {
        "message": "크롤링이 시작되었습니다",
        "pages": pages,
        "status": "started"
    }


@router.get("/status")
async def get_crawler_status():
    """크롤러 상태 조회"""
    return {
        "status": "ready",
        "message": "크롤러가 준비되었습니다",
        "supported_sites": ["대법원 경매정보"]
    }


async def perform_crawling(db: AsyncSession, pages: int = 3):
    """실제 크롤링 수행"""
    try:
        print("🕷️ 크롤링 시작...")
        
        # 크롤러 초기화
        crawler = CourtAuctionCrawler()
        matcher = KeywordMatcher()
        
        # 크롤링 실행
        crawled_items = await crawler.crawl_items(pages)
        
        # 키워드 매칭 및 알림 처리
        results = await matcher.process_crawled_items(db, crawled_items)
        
        print(f"✅ 크롤링 완료: {results}")
        
        # 크롤러 정리
        crawler.close()
        
    except Exception as e:
        print(f"❌ 크롤링 실패: {e}")
        raise 