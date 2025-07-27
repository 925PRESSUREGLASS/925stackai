

import os
import sys
from pathlib import Path


# --- Robust import for utils.kb_loader regardless of working directory ---
import importlib.util
import sys
from pathlib import Path
kb_loader_path = Path(__file__).resolve().parent.parent / "utils" / "kb_loader.py"
spec = importlib.util.spec_from_file_location("kb_loader", str(kb_loader_path))
kb_loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb_loader)
load_kb = kb_loader.load_kb
search_kb = kb_loader.search_kb

import streamlit as st

# Ensure project root is in sys.path for imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from agents.quote_agent import run_quote
from gui.components import parse_quote_output, render_quote


def main() -> None:

    st.set_page_config(page_title="Quote Assistant", layout="wide")
    st.title("Quoting Assistant")

    # --- Load Knowledge Base (KB) at startup ---
    if "kb" not in st.session_state:
        st.session_state.kb = load_kb("925stackai-KB")

    if "history" not in st.session_state:
        st.session_state.history = []

    from pathlib import Path

    import GPUtil
    import psutil
    from langchain_community.vectorstores import FAISS


    left, right = st.columns(2)

    # --- KB Search UI in sidebar ---
    with st.sidebar:
        st.header("Knowledge Base Search")
        kb_query = st.text_input("Search KB", key="kb_query")
        if kb_query:
            kb_results = search_kb(st.session_state.kb, kb_query)
            if kb_results:
                for title, content in kb_results:
                    st.markdown(f"### {title}")
                    st.markdown(content)
            else:
                st.info("No KB results found.")


    def generate_and_clear():
        prompt = st.session_state.get("prompt_input", "")
        if prompt.strip():
            output = run_quote(prompt.strip())
            data = parse_quote_output(output)
            st.session_state.history.append({"prompt": prompt.strip(), "data": data})
            # --- Store prompt and quote in data/quotes.jsonl and vector store ---
            import json
            from vector_store.quote_embedder import QuoteVectorStore
            quote_entry = {"prompt": prompt.strip(), "result": data}
            quotes_path = Path("data/quotes.jsonl")
            quotes_path.parent.mkdir(parents=True, exist_ok=True)
            with open(quotes_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(quote_entry, ensure_ascii=False) + "\n")
            # Add to vector store
            vs = QuoteVectorStore(data_path=str(quotes_path))
            vs.build_index()
        # Clear the input after quote generation
        st.session_state["prompt_input"] = ""


    with left:
        st.header("Chat")
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        user_input = st.chat_input('Ask a question or request a quote...')
        if user_input:
            # Determine if this is a quote request or KB/help query
            # For now, treat all as quote requests if not found in KB
            kb_results = search_kb(st.session_state.kb, user_input)
            if kb_results:
                response = kb_results[0][1]
            else:
                output = run_quote(user_input.strip())
                data = parse_quote_output(output)
                response = f"Quote total: ${data.get('total', 0)}"
                # Optionally, store in old history for right column quote display
                st.session_state.history.append({"prompt": user_input.strip(), "data": data})
            st.session_state['chat_history'].append({'user': user_input, 'assistant': response})

        for exchange in st.session_state['chat_history']:
            st.chat_message('user').write(exchange['user'])
            st.chat_message('assistant').write(exchange['assistant'])

        st.subheader("System Resource Usage")
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        st.write(f"CPU Usage: {cpu}%")
        st.write(
            f"Memory Usage: {mem.percent}% ({mem.used // (1024**2)} MB / {mem.total // (1024**2)} MB)"
        )
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                for gpu in gpus:
                    st.write(
                        f"GPU {gpu.id}: {gpu.name}, Load: {gpu.load*100:.1f}%, Mem: {gpu.memoryUsed}MB/{gpu.memoryTotal}MB"
                    )
            else:
                st.write("No GPU detected.")
        except Exception as e:
            st.write(f"GPU info unavailable: {e}")

        st.subheader("Vector Store Stats")
        try:
            from vector_store.quote_embedder import QuoteVectorStore
            quotes_path = Path("data/quotes.jsonl")
            vs = QuoteVectorStore(data_path=str(quotes_path))
            count = vs.count()
            st.write(f"Number of vectors: {count}")
        except Exception as e:
            st.write(f"Could not load vector store: {e}")

    with right:
        st.header("Quote")
        if st.session_state.history:
            render_quote(st.session_state.history[-1]["data"])
        else:
            st.write("Enter a job description to generate a quote.")


if __name__ == "__main__":
    main()
