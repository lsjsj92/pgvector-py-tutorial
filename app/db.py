from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text

from app.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

# PostgreSQL URL (asyncpg)
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# echo=True -> SQL 로그 출력
async_engine = create_async_engine(DATABASE_URL, echo=True)

# 세션 팩토리 (자동커밋/오토플러시 끔)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

async def init_db():
    """
    pgvector 확장을 활성화하고, Base에 정의된 모든 테이블을 생성
    """
    async with async_engine.begin() as conn:
        # pgvector extension
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        # 테이블 생성
        await conn.run_sync(Base.metadata.create_all)

# FastAPI 의존성 주입용
async def get_db_session():
    """
    DB 세션을 제공하는 Generator
    """
    async with AsyncSessionLocal() as session:
        yield session
