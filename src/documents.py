import shutil
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
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
    return (DB_FOLDER / "chroma.sqlite3").exists()


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

    if DB_FOLDER.exists():
        shutil.rmtree(DB_FOLDER)

    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(DB_FOLDER),
    )
    db.persist()
    return len(pdf_files), len(chunks)
