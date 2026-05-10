import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaEmbeddings, OllamaLLM

import os

# --- CONSTANTS & PATHS ---
# Find the src folder, then move one level up to the project root.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FOLDER = os.path.join(BASE_DIR, "data")
DB_FOLDER = os.path.join(BASE_DIR, "chroma_db")
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3"
K_RESULTS = 4

# --- UI CONFIGURATION ---
st.set_page_config(page_title="Financial RAG Assistant", page_icon="🏦")
st.title("🏦 Financial RAG Assistant")
st.markdown("Ask me anything about the financial documents you loaded.")

# --- RAG SYSTEM INITIALIZATION ---
# st.cache_resource loads the database and model only once.
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@st.cache_resource
def load_rag_chain():
    # 1. Reload the vector database.
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma(persist_directory=DB_FOLDER, embedding_function=embeddings)
    
    # 2. Configure the retriever.
    retriever = db.as_retriever(search_kwargs={"k": K_RESULTS})
    
    # 3. Initialize the large language model.
    llm = OllamaLLM(model=LLM_MODEL)
    
    # 4. Build a strict prompt to keep answers grounded in the retrieved documents.
    template = """You are an expert financial advisor.
    Use ONLY the following context excerpts retrieved from the documents to answer the question.
    If the answer is not contained in the context, answer: "I am sorry, but I could not find information about that in the loaded documents." Never invent figures or data.

    Context: {context}

    Question: {question}

    Answer:"""
    
    prompt_template = PromptTemplate(template=template, input_variables=["context", "question"])
    
    # 5. Combine retrieval, prompt, and model in a RAG pipeline.
    qa_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt_template
        | llm
        | StrOutputParser()
    )
    return qa_chain

# Load the system.
qa_chain = load_rag_chain()

# --- CHAT UI HANDLING ---
# Initialize the chat history in Streamlit session state.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input.
if prompt := st.chat_input("Example: What are the main risk factors mentioned?"):
    # Save and display the user message.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate the AI response.
    with st.chat_message("assistant"):
        with st.spinner("Searching the financial documents..."):
            try:
                # Run the RAG chain.
                response = qa_chain.invoke(prompt)
                
                # Display the response.
                st.markdown(response)
                
                # Save the response in the chat history.
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {e}")
