import gc
import html

import streamlit as st

from config import EMBEDDING_MODEL, K_RESULTS, LLM_MODEL
from documents import (
    index_exists,
    list_loaded_documents,
    rebuild_vector_index,
    remove_document,
    save_uploaded_documents,
)
from styles import APP_CSS


EXAMPLE_PROMPTS = [
    "Summarize the key financial risks.",
    "What macroeconomic assumptions are mentioned?",
    "List the most important figures and explain their context.",
]


def configure_page():
    st.set_page_config(
        page_title="Financial RAG Assistant",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(APP_CSS, unsafe_allow_html=True)


def render_document_card(document):
    document_name = html.escape(document["name"])
    document_size = html.escape(document["size"])
    sample_badge = '<div class="doc-badge">Bundled sample</div>' if document["is_sample"] else ""
    st.markdown(
        f"""
        <div class="doc-row">
            <div class="doc-name">{document_name}</div>
            <div class="doc-meta">{document_size} - PDF</div>
            {sample_badge}
        </div>
        """,
        unsafe_allow_html=True,
    )


def mark_index_stale():
    st.session_state.index_dirty = True
    st.session_state.active_prompt = None
    st.session_state.is_generating = False


def render_sidebar(on_index_rebuilt):
    documents = list_loaded_documents()
    db_ready = index_exists()
    index_dirty = st.session_state.index_dirty

    with st.sidebar:
        st.markdown("## Financial RAG")
        if index_dirty:
            status_class = "status-stale"
            status_text = "Rebuild required"
        elif db_ready:
            status_class = "status-ready"
            status_text = "Index ready"
        else:
            status_class = "status-missing"
            status_text = "Index missing"

        st.markdown(
            f'<span class="status-pill {status_class}">{status_text}</span>',
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)
        col_a.metric("PDFs", len(documents))
        col_b.metric(
            "Context passages",
            K_RESULTS,
            help="Number of retrieved document passages used to answer each question.",
        )

        st.divider()
        st.markdown("### Documents")

        if documents:
            for document in documents:
                doc_col, action_col = st.columns([0.82, 0.18], vertical_alignment="center")
                with doc_col:
                    render_document_card(document)
                with action_col:
                    if st.button(
                        "\u00d7",
                        key=f"remove_document_{document['name']}",
                        help=f"Remove {document['name']}",
                        type="primary",
                        use_container_width=True,
                    ):
                        if remove_document(document["name"]):
                            mark_index_stale()
                            st.warning(f"Removed {document['name']}. Rebuild the index before asking new questions.")
                            st.rerun()
                        else:
                            st.error("The selected file could not be removed.")
        else:
            st.info("No PDF files found in data/.")

        uploaded_files = st.file_uploader(
            "Upload PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            help="Uploaded files are saved in the local document folder.",
        )
        if uploaded_files and st.button("Add uploaded PDFs", use_container_width=True):
            saved_files = save_uploaded_documents(uploaded_files)
            if saved_files:
                mark_index_stale()
                st.success(f"Added {len(saved_files)} PDF file(s). Rebuild the index before asking new questions.")
                st.rerun()
            else:
                st.warning("No valid PDF files were uploaded.")

        st.divider()
        if index_dirty:
            st.warning("The document set changed. Rebuild the index to continue asking questions.")

        if st.button("Rebuild document index", type="primary", use_container_width=True):
            with st.spinner("Rebuilding the vector index..."):
                try:
                    on_index_rebuilt()
                    gc.collect()
                    file_count, chunk_count = rebuild_vector_index()
                    st.session_state.index_dirty = False
                    on_index_rebuilt()
                    gc.collect()
                    st.success(f"Indexed {file_count} PDF file(s) into {chunk_count} chunks.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Index rebuild failed: {exc}")

        st.divider()
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.rerun()

        st.caption(f"LLM: {LLM_MODEL}")
        st.caption(f"Embeddings: {EMBEDDING_MODEL}")


def render_header():
    st.markdown(
        """
        <div class="hero-panel">
            <div class="app-kicker">Local financial document intelligence</div>
            <div class="app-title">Financial RAG Assistant</div>
            <div class="app-subtitle">
                Upload financial PDFs, rebuild the local index, and ask grounded questions over your private document set.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def init_chat_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None

    if "active_prompt" not in st.session_state:
        st.session_state.active_prompt = None

    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False

    if "index_dirty" not in st.session_state:
        st.session_state.index_dirty = False


def render_quick_prompts():
    prompt_cols = st.columns(len(EXAMPLE_PROMPTS))
    disabled = st.session_state.is_generating or st.session_state.index_dirty
    for col, example in zip(prompt_cols, EXAMPLE_PROMPTS):
        if col.button(example, use_container_width=True, disabled=disabled):
            st.session_state.active_prompt = example
            st.session_state.is_generating = True
            st.rerun()


def render_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def get_current_prompt():
    prompt = st.chat_input(
        "Example: What are the main risk factors mentioned?",
        disabled=st.session_state.is_generating or st.session_state.index_dirty,
    )
    if prompt and not st.session_state.is_generating:
        st.session_state.active_prompt = prompt
        st.session_state.is_generating = True
        st.rerun()


def render_chat_response(qa_chain, prompt):
    with st.chat_message("assistant"):
        if qa_chain is None:
            response = "The document index is not ready yet. Upload one or more PDFs, then click **Rebuild document index** in the sidebar."
            st.warning(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.active_prompt = None
            st.session_state.is_generating = False
            return

        stop_button = st.empty()
        stop_requested = stop_button.button("Stop generation", key="stop_generation", use_container_width=False)
        if stop_requested:
            stop_button.empty()
            st.session_state.active_prompt = None
            st.session_state.is_generating = False
            st.session_state.messages.append({"role": "assistant", "content": "Generation stopped."})
            st.rerun()

        response_placeholder = st.empty()
        response = ""
        completed = False

        try:
            with st.spinner("Searching the financial documents..."):
                for chunk in qa_chain.stream(prompt):
                    response += chunk
                    response_placeholder.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})
            completed = True
        except Exception as exc:
            st.error(f"An error occurred: {exc}")
        finally:
            stop_button.empty()
            st.session_state.active_prompt = None
            st.session_state.is_generating = False
            if completed:
                st.rerun()


def handle_chat(qa_chain):
    if st.session_state.index_dirty:
        st.warning("Rebuild the document index before asking another question.")

    render_quick_prompts()
    render_chat_history()
    get_current_prompt()

    prompt = st.session_state.active_prompt
    if not prompt:
        return

    should_append_user_message = not (
        st.session_state.messages
        and st.session_state.messages[-1]["role"] == "user"
        and st.session_state.messages[-1]["content"] == prompt
    )

    if should_append_user_message:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    render_chat_response(qa_chain, prompt)
