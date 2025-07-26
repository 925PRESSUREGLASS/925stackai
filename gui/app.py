
import os
import sys
from pathlib import Path

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

    if "history" not in st.session_state:
        st.session_state.history = []

    from pathlib import Path

    import GPUtil
    import psutil
    from langchain_community.vectorstores import FAISS

    left, right = st.columns(2)

    def generate_and_clear():
        prompt = st.session_state.get("prompt_input", "")
        if prompt.strip():
            output = run_quote(prompt.strip())
            data = parse_quote_output(output)
            st.session_state.history.append({"prompt": prompt.strip(), "data": data})
        st.session_state["prompt_input"] = ""

    with left:
        st.header("Chat History")
        for entry in st.session_state.history:
            st.write(f"**You:** {entry['prompt']}")
            st.write(f"**Total:** {entry['data'].get('total', 0)}")
        st.text_area("Describe the job", key="prompt_input")
        st.button("Generate Quote", on_click=generate_and_clear)

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
        vector_path = Path("vector_store")
        if (vector_path / "index.faiss").exists():
            try:
                store = FAISS.load_local(
                    str(vector_path), None, allow_dangerous_deserialization=True
                )
                st.write(f"Number of vectors: {len(store.index_to_docstore_id)}")
            except Exception as e:
                st.write(f"Could not load vector store: {e}")
        else:
            st.write("No vector store found.")

    with right:
        st.header("Quote")
        if st.session_state.history:
            render_quote(st.session_state.history[-1]["data"])
        else:
            st.write("Enter a job description to generate a quote.")


if __name__ == "__main__":
    main()
