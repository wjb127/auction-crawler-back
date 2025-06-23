from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.config import settings
import asyncpg

# 동기 엔진 (마이그레이션용)
engine = create_engine(settings.database_url)

# 비동기 엔진 (FastAPI용)
async_database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(async_database_url, echo=True)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Base 클래스
Base = declarative_base()

# 메타데이터
metadata = MetaData()


# 데이터베이스 세션 의존성
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# 데이터베이스 연결 테스트
async def test_database_connection():
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
        print("✅ 데이터베이스 연결 성공!")
        return True
    except Exception as e:
        print(f"❌ 데이터베이스 연결 실패: {e}")
        return False 