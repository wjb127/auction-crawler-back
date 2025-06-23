from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from datetime import datetime
import asyncio

# 임시 메모리 저장소
memory_keywords = []
memory_detected_items = []
memory_alerts = []

# FastAPI 앱 생성
app = FastAPI(
    title="경매 알림 SaaS API",
    version="1.0.0",
    description="경매 알림 SaaS 백엔드 API (테스트 버전)",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "경매 알림 SaaS API (테스트 버전)",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "message": "API가 정상 작동 중입니다",
        "version": "1.0.0"
    }

# 키워드 관리 API
@app.get("/keywords")
async def get_keywords(user_id: str) -> List[Dict[str, Any]]:
    """사용자의 키워드 목록 조회"""
    user_keywords = [k for k in memory_keywords if k["user_id"] == user_id]
    return user_keywords

@app.post("/keywords")
async def create_keyword(keyword_data: Dict[str, str]) -> Dict[str, Any]:
    """새 키워드 등록"""
    new_keyword = {
        "id": len(memory_keywords) + 1,
        "user_id": keyword_data["user_id"],
        "keyword": keyword_data["keyword"],
        "created_at": datetime.now().isoformat()
    }
    memory_keywords.append(new_keyword)
    return new_keyword

@app.delete("/keywords/{keyword_id}")
async def delete_keyword(keyword_id: int):
    """키워드 삭제"""
    global memory_keywords
    memory_keywords = [k for k in memory_keywords if k["id"] != keyword_id]
    return {"message": "키워드가 삭제되었습니다"}

# 감지된 경매 물건 API
@app.get("/detected")
async def get_detected_items(keyword: str = None, limit: int = 50) -> List[Dict[str, Any]]:
    """감지된 경매 물건 목록 조회"""
    items = memory_detected_items[:limit]
    if keyword:
        items = [item for item in items if keyword.lower() in item["title"].lower()]
    return items

@app.get("/detected/{item_id}")
async def get_detected_item(item_id: int) -> Dict[str, Any]:
    """감지된 경매 물건 상세 조회"""
    for item in memory_detected_items:
        if item["id"] == item_id:
            return item
    return {"error": "경매 물건을 찾을 수 없습니다"}

# 알림 기록 API
@app.get("/alerts")
async def get_alerts(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """사용자별 알림 기록 조회"""
    user_alerts = [a for a in memory_alerts if a["user_id"] == user_id]
    return user_alerts[:limit]

# 크롤링 API
@app.post("/crawler/run")
async def run_crawler(pages: int = 3) -> Dict[str, Any]:
    """수동 크롤링 실행 (테스트용 더미 데이터)"""
    # 테스트용 더미 데이터 생성
    dummy_items = [
        {
            "id": len(memory_detected_items) + 1,
            "title": "서울특별시 송파구 잠실동 123-45 아파트",
            "appraisal_value": 850000000,
            "bid_date": "2024-02-15",
            "url": "https://example-auction-site.com/item/12345",
            "keywords": ["송파구", "아파트"],
            "source_site": "대법원 경매정보",
            "created_at": datetime.now().isoformat()
        },
        {
            "id": len(memory_detected_items) + 2,
            "title": "부산광역시 강서구 명지동 567-89 오피스텔",
            "appraisal_value": 450000000,
            "bid_date": "2024-02-20",
            "url": "https://example-auction-site.com/item/12346",
            "keywords": ["부산", "강서구", "오피스텔"],
            "source_site": "대법원 경매정보",
            "created_at": datetime.now().isoformat()
        }
    ]
    
    memory_detected_items.extend(dummy_items)
    
    return {
        "message": "크롤링이 완료되었습니다 (테스트용 더미 데이터)",
        "pages": pages,
        "status": "completed",
        "new_items": len(dummy_items)
    }

@app.get("/crawler/status")
async def get_crawler_status():
    """크롤러 상태 조회"""
    return {
        "status": "ready",
        "message": "크롤러가 준비되었습니다 (테스트 모드)",
        "supported_sites": ["대법원 경매정보"],
        "total_items": len(memory_detected_items),
        "total_keywords": len(memory_keywords),
        "total_alerts": len(memory_alerts)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 