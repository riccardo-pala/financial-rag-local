# Financial RAG Assistant

Financial RAG Assistant is a local Retrieval Augmented Generation application for asking questions about financial PDF documents. It combines local PDF processing, Chroma vector search, Ollama, LangChain, and a Streamlit chat interface.

The app is designed for private document analysis: reports, prospectuses, compliance documents, policy material, and market research notes can be explored locally without sending their content to hosted AI services.

## Highlights

- Upload and remove PDF documents from the web interface.
- Rebuild the document index from the sidebar.
- Ask document-grounded questions through a chat UI.
- Run Llama 3 locally through Ollama.
- Generate embeddings locally with Nomic Embed Text.
- Test the app immediately with the included sample PDF.

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.ai) installed and running
- Required Ollama models:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

## Quick Start

Clone the repository:

```bash
git clone https://github.com/riccardo-pala/financial-rag.git
cd financial-rag
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

Start Ollama:

```bash
ollama serve
```

Run the app:

```bash
streamlit run src/app.py
```

Open `http://localhost:8501`.

## Using The App

The sidebar is the document control panel:

- **Upload PDFs** adds new documents to the local document folder.
- **Remove selected PDF** removes a document from the local document folder.
- **Rebuild document index** refreshes the vector index after uploads or removals.
- The document list shows which PDFs are currently available for analysis.

After the index is ready, use the chat input to ask questions about the indexed PDFs. The app also includes quick prompt buttons for common financial review tasks.

## Optional CLI Ingestion

You can also add PDFs manually and build the index from the command line:

```bash
mkdir -p data
cp /path/to/your/documents/*.pdf data/
python src/ingest.py
```

Then start the app:

```bash
streamlit run src/app.py
```

## Configuration

Main settings live near the top of the Python files.

In `src/app.py`:

```python
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3"
K_RESULTS = 4
```

In `src/ingest.py`:

```python
DATA_FOLDER = "data"
DB_FOLDER = "chroma_db"
EMBEDDING_MODEL = "nomic-embed-text"
```

To use a different local model, pull it with Ollama and update `LLM_MODEL`.

## Privacy

- Documents remain on your machine.
- Embeddings are generated locally through Ollama.
- The vector index is stored locally.
- The application does not intentionally send document content to hosted LLM APIs.

## Limitations

- Only PDF documents are currently supported.
- OCR is not included, so scanned PDFs may require preprocessing.
- Answers depend on the quality of PDF text extraction and retrieval.
- The app does not currently show source citations in the chat.
- Generated answers are not financial advice.

## Troubleshooting

### Ollama is not running

Start Ollama:

```bash
ollama serve
```

Then verify that the models are available:

```bash
ollama list
```

### Model not found

Pull the required models:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### Uploaded documents are not used in answers

Click **Rebuild document index** in the sidebar after uploading or removing PDFs.

### Answers are incomplete or not relevant

- Rebuild the document index after changing the document set.
- Try asking a more specific question.
- Increase `K_RESULTS` in `src/app.py` to retrieve more context.
- Check whether the PDF contains extractable text.

## Disclaimer

This project is intended for local document exploration and research support. It does not provide investment, legal, accounting, or compliance advice. Always verify important outputs against the original source documents.

## License

This project is published for portfolio and interview purposes. No reuse license is currently granted.
