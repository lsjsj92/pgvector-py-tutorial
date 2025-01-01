from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models import TextItem
from app.db import get_db_session
from app.models import TextItem
from app.schemas import TextItemCreate, TextItemResponse
from app.embeddings import get_embedding

router = APIRouter()

@router.post("/create-item", response_model=TextItemResponse, tags=["Items"])
def create_text_item(
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
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/items/{item_id}", response_model=TextItemResponse, tags=["Items"])
def get_text_item(item_id: int, db: Session = Depends(get_db_session)):
    """
    특정 ID로 텍스트 조회
    """
    db_item = db.query(TextItem).filter(TextItem.id == item_id).first()
    if not db_item:
        return {"error": "Item not found"}  # 혹은 HTTPException(404, ...)
    return db_item

# 1) TITLE 검색(정확 일치)
@router.get("/search/title", response_model=List[TextItemResponse], tags=["Search"])
def search_by_title(title: str, db: Session = Depends(get_db_session)):
    """
    title이 Exact Match인 레코드를 리스트로 반환
    """
    results = db.query(TextItem).filter(TextItem.title == title).all()
    return results

# 2) 시맨틱 검색
@router.get("/search/semantic", tags=["Search"])
def semantic_search(query: str, limit: int = 5, db: Session = Depends(get_db_session)):
    """
    1) query 문자열을 임베딩 (HuggingFace Hub)
    2) pgvector 메서드 방식 (cosine_distance)로 오름차순 정렬
    3) 상위 limit개 반환
    """
    # (1) 임베딩
    query_embedding = get_embedding(query)

    # (2) 메서드 방식 사용
    #     TextItem.embed.cosine_distance(query_embedding)
    results = (
        db.query(TextItem)
        .order_by(TextItem.embed.cosine_distance(query_embedding))
        .limit(limit)
        .all()
    )

    # (3) 결과를 dict로 변환
    return [
        {
            "id": r.id,
            "title": r.title,
            "content": r.content
        }
        for r in results
    ]
