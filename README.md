# Financial RAG Assistant

Financial RAG Assistant is a local Retrieval Augmented Generation application for querying financial documents with open-source models. It combines PDF ingestion, local embeddings, Chroma vector search, Ollama, LangChain, and a Streamlit chat interface.

The project is designed for private analysis of reports, prospectuses, policy documents, compliance material, and market research notes without sending document content to external AI services.

## Highlights

- Local-first RAG workflow for PDF documents.
- Offline LLM inference through Ollama and Llama 3.
- Local embedding generation with Nomic Embed Text.
- Persistent Chroma vector database stored on disk.
- Streamlit chat UI for document-grounded questions.
- Strict prompt behavior that avoids answering outside the retrieved context.

## Architecture

```text
PDF files
   |
   v
src/ingest.py
   |  load PDFs, split text, generate embeddings
   v
chroma_db/
   |
   v
src/app.py
   |  retrieve relevant chunks, build prompt, call Ollama
   v
Streamlit chat UI
```

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.ai) installed and running
- The required Ollama models:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

## Quick Start

Clone the repository:

```bash
git clone https://github.com/riccardo-pala/financial-rag-local.git
cd financial-rag-local
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure Ollama is running:

```bash
ollama serve
```

In another terminal, verify the models:

```bash
ollama list
```

## Usage

Create a `data/` directory and add your PDF files:

```bash
mkdir -p data
cp /path/to/your/documents/*.pdf data/
```

Run the ingestion pipeline:

```bash
python src/ingest.py
```

Expected output:

```text
Starting the ingestion process...
Loading: document1.pdf...
Loaded 150 pages in total.
Documents split into 500 chunks.
Generating vectors with Ollama (nomic-embed-text) and saving them to ChromaDB...
Ingestion completed successfully. The database is ready in 'chroma_db/'.
```

Start the Streamlit app:

```bash
streamlit run src/app.py
```

Open `http://localhost:8501` and ask questions about the indexed documents.

## Configuration

The main runtime parameters are defined near the top of the Python files.

In `src/ingest.py`:

```python
DATA_FOLDER = "data"
DB_FOLDER = "chroma_db"
EMBEDDING_MODEL = "nomic-embed-text"
```

In `src/app.py`:

```python
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3"
K_RESULTS = 4
```

To use a different local model, pull it with Ollama and update `LLM_MODEL`.

## Project Structure

```text
financial-rag-local/
|-- data/                    # Local PDF files, ignored by Git
|-- chroma_db/               # Local vector database, ignored by Git
|-- src/
|   |-- app.py               # Streamlit RAG chat application
|   `-- ingest.py            # PDF ingestion and embedding pipeline
|-- .gitignore
|-- requirements.txt         # Direct project dependencies
|-- requirements-lock.txt    # Locked dependency snapshot
`-- README.md
```

## Dependency Files

Use `requirements.txt` for regular setup.

Use `requirements-lock.txt` when you need a more reproducible environment:

```bash
pip install -r requirements-lock.txt
```

## Privacy and Data Handling

- Documents remain on your machine.
- Embeddings are generated locally through Ollama.
- The vector database is stored locally in `chroma_db/`.
- `data/` and `chroma_db/` are ignored by Git to avoid committing private documents or generated indexes.
- No document content is intentionally sent to hosted LLM APIs by this application.

## Limitations

- Only PDF ingestion is currently supported.
- OCR is not included, so scanned PDFs may require preprocessing.
- Answers depend on the quality of PDF extraction and retrieved chunks.
- The app does not currently show source citations in the UI.
- The generated answers are not financial advice.

## Troubleshooting

### Ollama is not running

Start Ollama:

```bash
ollama serve
```

Then verify that the server responds:

```bash
ollama list
```

### Model not found

Pull the required models:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### No documents are found

Make sure PDF files exist in the `data/` directory:

```bash
ls data/
```

Then rerun ingestion:

```bash
python src/ingest.py
```

### Answers are incomplete or not relevant

- Re-run ingestion after adding or replacing documents.
- Increase `K_RESULTS` in `src/app.py` to retrieve more context.
- Improve the prompt template in `src/app.py` for your document type.
- Check whether the source PDFs contain extractable text.

### Chroma warnings

Some LangChain or Chroma versions may emit deprecation warnings. They are usually non-blocking. If they become errors, update the Chroma integration and imports according to the installed package versions.

## Roadmap

- Add source citations and document metadata in answers.
- Support DOCX, TXT, and Markdown files.
- Add OCR support for scanned PDFs.
- Add document-level filters.
- Add persisted chat history.
- Add automated tests for ingestion and RAG pipeline setup.

## Contributing

Contributions are welcome. Before opening a pull request:

1. Keep private documents out of the repository.
2. Run the ingestion flow with a small sample PDF.
3. Start the Streamlit app and verify that questions can be answered.
4. Keep changes focused and document any new configuration.

## Disclaimer

This project is intended for local document exploration and research support. It does not provide investment, legal, accounting, or compliance advice. Always verify important outputs against the original source documents.

## License

This project is published for portfolio and interview purposes. No reuse license is currently granted.
