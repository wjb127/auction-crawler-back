from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app.config import settings
from app.database import test_database_connection, Base, async_engine
from app.api import keywords_router, detected_router, alerts_router
from app.api.crawler import router as crawler_router

# FastAPI 앱 생성
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="경매 알림 SaaS 백엔드 API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(keywords_router)
app.include_router(detected_router)
app.include_router(alerts_router)
app.include_router(crawler_router)


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    print("🚀 경매 알림 SaaS API 시작 중...")
    
    # 데이터베이스 연결 테스트
    success = await test_database_connection()
    if not success:
        print("❌ 경고: 데이터베이스 연결에 실패했습니다. 환경 변수를 확인하세요.")
    
    print(f"📖 API 문서: http://localhost:8000/docs")
    print(f"🔧 환경: {settings.environment}")


@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    print("🛑 경매 알림 SaaS API 종료 중...")


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "경매 알림 SaaS API",
        "version": settings.api_version,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    try:
        # 데이터베이스 연결 테스트
        db_status = await test_database_connection()
        return {
            "status": "healthy" if db_status else "unhealthy",
            "database": "connected" if db_status else "disconnected",
            "version": settings.api_version
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e),
            "version": settings.api_version
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False
    ) 