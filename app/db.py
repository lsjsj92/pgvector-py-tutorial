from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

# PostgreSQL + Psycopg2
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """
    pgvector 확장을 활성화하고, Base에 정의된 모든 테이블을 생성합니다.
    """
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """
    매 요청마다 사용할 세션을 제공하기 위한 의존성 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
