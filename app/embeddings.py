from typing import List
from langchain.embeddings import HuggingFaceHubEmbeddings
from app.config import HF_EMBED_REPO_ID

# LangChain으로 Hugging Face Embeddings 사용
hf_embeddings = HuggingFaceHubEmbeddings(repo_id=HF_EMBED_REPO_ID)

def get_embedding(text: str) -> List[float]:
    """
    입력 텍스트를 Hugging Face Hub Embeddings로 변환한 후, 벡터(list[float])를 반환
    """
    return hf_embeddings.embed_query(text)
