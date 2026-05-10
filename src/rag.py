import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaEmbeddings, OllamaLLM

from config import DB_FOLDER, EMBEDDING_MODEL, K_RESULTS, LLM_MODEL


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


@st.cache_resource
def load_rag_chain():
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    db = Chroma(persist_directory=str(DB_FOLDER), embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": K_RESULTS})
    llm = OllamaLLM(model=LLM_MODEL)

    prompt_template = PromptTemplate(
        template="""You are an expert financial advisor.
        Use ONLY the following context excerpts retrieved from the documents to answer the question.
        If the answer is not contained in the context, answer: "I am sorry, but I could not find information about that in the loaded documents." Never invent figures or data.

        Context: {context}

        Question: {question}

        Answer:""",
        input_variables=["context", "question"],
    )

    return (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt_template
        | llm
        | StrOutputParser()
    )
