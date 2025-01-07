from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import TextItem
from app.db import get_db_session
from app.models import TextItem
from app.schemas import TextItemCreate, TextItemResponse
from app.embeddings import get_embedding

router = APIRouter()

@router.post("/create-item", response_model=TextItemResponse, tags=["Items"])
async def create_text_item(
    item: TextItemCreate,
    db: Session = Depends(get_db_session)
):
    """
    입력 텍스트(title, content)를 임베딩 후 PostgreSQL에 저장
    """
    vector = get_embedding(item.content)  # content 임베딩
    db_item = TextItem(
        title=item.title,
        content=item.content,
        embed=vector
    )
    db.add(db_item)
    
    await db.commit()
    await db.refresh(db_item)
    
    return db_item

@router.get("/items/{item_id}", response_model=TextItemResponse, tags=["Items"])
async def get_text_item(item_id: int, db: AsyncSession = Depends(get_db_session)):
    """
    특정 ID 텍스트 조회
    """
    result = await db.execute(select(TextItem).where(TextItem.id == item_id))
    db_item = result.scalars().first()
    
    if not db_item:
        return {"error": "Item not found"}
    
    return db_item

@router.get("/search/title", response_model=List[TextItemResponse], tags=["Search"])
async def search_by_title(title: str, db: AsyncSession = Depends(get_db_session)):
    """
    title이 Exact Match인 레코드를 리스트로 반환
    """
    # 1) SELECT 쿼리 준비
    stmt = select(TextItem).where(TextItem.title == title)
    
    # 2) 실행
    result = await db.execute(stmt)
    
    # 3) Query 결과
    items = result.scalars().all()
    # print(items)
    # print(items[0].title)
    
    return items

@router.get("/search/semantic", tags=["Search"])
async def semantic_search(query: str, limit: int = 5, db: AsyncSession = Depends(get_db_session)):
    """
    1) query 문자열을 임베딩 (HuggingFace Hub)
    2) pgvector 메서드 방식 (cosine_distance)로 오름차순 정렬
    3) 상위 limit개 반환
    """
    # (1) 임베딩
    query_embedding = get_embedding(query)

    # (2) 검색
    stmt = (
        select(TextItem)
        .order_by(TextItem.embed.cosine_distance(query_embedding))
        .limit(limit)
    )
    # 쿼리 실행
    result = await db.execute(stmt)

    # (3) 결과 추출
    items = result.scalars().all()

    # (4) dict로 변환
    return [
        {
            "id": r.id,
            "title": r.title,
            "content": r.content
        }
        for r in items
    ]
