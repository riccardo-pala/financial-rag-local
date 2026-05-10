from datetime import datetime
from pathlib import Path
from uuid import uuid4

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    ACTIVE_INDEX_FILE,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    DATA_FOLDER,
    DB_FOLDER,
    EMBEDDING_MODEL,
    SAMPLE_DOCUMENTS,
)


def format_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    return f"{size_bytes / (1024 * 1024):.1f} MB"


def index_exists():
    return (get_active_index_path() / "chroma.sqlite3").exists()


def get_active_index_path():
    if ACTIVE_INDEX_FILE.exists():
        index_name = ACTIVE_INDEX_FILE.read_text().strip()
        if index_name:
            return DB_FOLDER / index_name

    # Backward compatibility with older single-folder Chroma indexes.
    return DB_FOLDER


def create_next_index_path():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return DB_FOLDER / f"index_{timestamp}_{uuid4().hex[:8]}"


def set_active_index_path(index_path):
    DB_FOLDER.mkdir(parents=True, exist_ok=True)
    ACTIVE_INDEX_FILE.write_text(index_path.name)


def list_loaded_documents():
    if not DATA_FOLDER.exists():
        return []

    documents = []
    for file_path in sorted(DATA_FOLDER.glob("*.pdf")):
        documents.append(
            {
                "name": file_path.name,
                "path": file_path,
                "size": format_file_size(file_path.stat().st_size),
                "is_sample": file_path.name in SAMPLE_DOCUMENTS,
            }
        )
    return documents


def save_uploaded_documents(uploaded_files):
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    saved_files = []
    for uploaded_file in uploaded_files:
        file_name = Path(uploaded_file.name).name
        if not file_name.lower().endswith(".pdf"):
            continue

        destination = DATA_FOLDER / file_name
        destination.write_bytes(uploaded_file.getbuffer())
        saved_files.append(file_name)

    return saved_files


def remove_document(file_name):
    target = DATA_FOLDER / Path(file_name).name
    if target.exists() and target.is_file():
        target.unlink()
        return True
    return False


def load_pdf_documents(pdf_files):
    documents = []
    for file_path in pdf_files:
        loader = PyPDFLoader(str(file_path))
        documents.extend(loader.load())
    return documents


def rebuild_vector_index():
    pdf_files = sorted(DATA_FOLDER.glob("*.pdf")) if DATA_FOLDER.exists() else []
    if not pdf_files:
        raise ValueError("Add at least one PDF before rebuilding the index.")

    documents = load_pdf_documents(pdf_files)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = text_splitter.split_documents(documents)

    DB_FOLDER.mkdir(parents=True, exist_ok=True)
    next_index_path = create_next_index_path()
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(next_index_path),
    )
    db.persist()
    set_active_index_path(next_index_path)
    return len(pdf_files), len(chunks)
