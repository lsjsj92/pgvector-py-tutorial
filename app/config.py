import os

# DB 연결 정보. 실제로는 .env 등을 사용해 관리하시는 것을 권장합니다.
DB_USER = os.getenv("DB_USER", "leesoojin")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "test")

# HuggingFace Embeddings (langchain) 설정
HF_EMBED_REPO_ID = os.getenv("HF_EMBED_REPO_ID", "sentence-transformers/all-MiniLM-l6-v2")
