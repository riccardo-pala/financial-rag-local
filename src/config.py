from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FOLDER = BASE_DIR / "data"
DB_FOLDER = BASE_DIR / "chroma_db"

EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3"

K_RESULTS = 4
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

SAMPLE_DOCUMENTS = {"en-bolleco-BCE-2-2026.pdf"}
