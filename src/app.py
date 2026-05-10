from documents import index_exists
from rag import load_rag_chain
from ui import configure_page, handle_chat, init_chat_state, render_header, render_sidebar


def main():
    configure_page()
    init_chat_state()

    render_sidebar(on_index_rebuilt=load_rag_chain.clear)
    render_header()

    qa_chain = load_rag_chain() if index_exists() else None
    handle_chat(qa_chain)


if __name__ == "__main__":
    main()
