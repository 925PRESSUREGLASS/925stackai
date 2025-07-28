

import os
import sys
from pathlib import Path


# --- Simplified import for utils.kb_loader ---
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.kb_loader import load_kb, search_kb

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
            # --- Spec grading ---
            from core.demo_spec_grading import grade_quote_response
            grading = grade_quote_response(prompt.strip(), output)
            st.session_state.history.append({"prompt": prompt.strip(), "data": data, "grading": grading})
            # --- Store prompt and quote in data/quotes.jsonl and vector store ---
            import json
            from vector_store.quote_embedder import QuoteVectorStore
            quote_entry = {"prompt": prompt.strip(), "result": data, "grading": grading}
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
                from core.demo_spec_grading import grade_quote_response
                grading = grade_quote_response(user_input.strip(), output)
                # --- Custom spec grading display ---
                score = grading['score']
                passed = grading['passed']
                failures = grading['failures']
                badge_color = 'green' if score == 1.0 else ('orange' if score >= 0.67 else 'red')
                badge = f"<span style='background-color:{badge_color};color:white;padding:4px 10px;border-radius:8px;font-weight:bold;'>Spec Score: {score}</span>"
                passed_str = ', '.join(passed) if passed else 'None'
                failed_str = ', '.join(failures) if failures else 'None'
                tooltip = "<span title='Passed: {} | Failed: {}'>ℹ️</span>".format(passed_str, failed_str)
                assistant_msg = f"Quote total: ${data.get('total', 0)}<br>{badge} {tooltip}<br><b>Passed:</b> {passed_str}<br><b>Failed:</b> {failed_str}"
                st.session_state['chat_history'].append({
                    'user': user_input.strip(),
                    'assistant': assistant_msg
                })
                st.session_state.history.append({"prompt": user_input.strip(), "data": data})

        for exchange in st.session_state['chat_history']:
            st.chat_message('user').write(exchange['user'])
            st.chat_message('assistant').markdown(exchange['assistant'], unsafe_allow_html=True)

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
            if count == 0:
                st.warning("Vector store is empty or failed to load. Check if 'data/quotes.jsonl' exists and is populated.")
            else:
                st.write(f"Number of vectors: {count}")
        except Exception as e:
            import traceback
            st.error(f"Could not load vector store: {e}")
            st.code(traceback.format_exc(), language="python")

    with right:
        st.header("Quote")
        if st.session_state.history:
            render_quote(st.session_state.history[-1]["data"])
        else:
            st.write("Enter a job description to generate a quote.")


if __name__ == "__main__":
    main()
