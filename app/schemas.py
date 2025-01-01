from pydantic import BaseModel

class TextItemCreate(BaseModel):
    title: str
    content: str

class TextItemResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True
