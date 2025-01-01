from sqlalchemy import Column, Integer, Text, String
from pgvector.sqlalchemy import Vector
from app.db import Base

class TextItem(Base):
    __tablename__ = "text_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)   # 제목
    content = Column(Text, nullable=False)   # 본문
    embed = Column(Vector(384), nullable=False)  # 384차원 벡터
