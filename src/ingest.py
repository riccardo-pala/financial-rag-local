from config import DATA_FOLDER
from documents import list_loaded_documents, rebuild_vector_index


def ingest_documents():
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    documents = list_loaded_documents()

    if not documents:
        print("No PDF files found in the data/ folder.")
        return

    print("Starting the ingestion process...")
    for document in documents:
        print(f"Loading: {document['name']}...")

    file_count, chunk_count = rebuild_vector_index()
    print(f"Indexed {file_count} PDF file(s) into {chunk_count} chunks.")
    print("Ingestion completed successfully. The database is ready in 'chroma_db/'.")


if __name__ == "__main__":
    ingest_documents()
