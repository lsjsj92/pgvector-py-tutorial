from fastapi import FastAPI
from app.db import init_db
from app.routers.health import router as health_router
from app.routers.items import router as items_router

def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI with PostgreSQL(pgvector) Example")

    # DB 초기화
    init_db()

    # 라우터 등록
    app.include_router(health_router)
    app.include_router(items_router)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
