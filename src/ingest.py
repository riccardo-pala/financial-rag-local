import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Constants
DATA_FOLDER = "data"
DB_FOLDER = "chroma_db"
EMBEDDING_MODEL = "nomic-embed-text"  # Previously downloaded embedding model.

def ingest_documents():
    print("Starting the ingestion process...")
    
    # 1. Load all PDF files from the data/ folder.
    pdf_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found in the data/ folder.")
        return

    documents = []
    for file in pdf_files:
        file_path = os.path.join(DATA_FOLDER, file)
        print(f"Loading: {file}...")
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
        
    print(f"Loaded {len(documents)} pages in total.")

    # 2. Split the text into chunks.
    # Use 1000 characters per chunk with 200 characters of overlap to preserve context.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Documents split into {len(chunks)} chunks.")

    # 3. Create embeddings locally with Ollama.
    print(f"Generating vectors with Ollama ({EMBEDDING_MODEL}) and saving them to ChromaDB...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    # Create and save the vector database to disk.
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=DB_FOLDER
    )
    
    # Force persistence to disk for Chroma versions that require it.
    db.persist()
    print("Ingestion completed successfully. The database is ready in 'chroma_db/'.")

if __name__ == "__main__":
    # Ensure the data folder exists.
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
        print(f"Folder '{DATA_FOLDER}' created. Add your PDF files and run the script again.")
    else:
        ingest_documents()
