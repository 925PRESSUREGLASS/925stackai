import streamlit as st
from llama3_model.model import Llama3QuoteModel

st.set_page_config(page_title="Llama3 Quoting Assistant", layout="centered")
st.title("Llama3 Quoting Assistant 🦙💬")

if "model" not in st.session_state:
    st.session_state.model = Llama3QuoteModel()

st.markdown(
    """
Enter a description of the quote you need. The assistant will generate a quote using the local Llama 3 model (Ollama) if available, or fallback to the local PyTorch model.
"""
)

system_prompt = st.text_area(
    "System Prompt (optional)", "You are a helpful quoting assistant."
)
user_message = st.text_area(
    "Quote Description", "I need a quote for replacing 10 windows in a two-story house."
)
max_tokens = st.slider("Max New Tokens", 32, 512, 128)

if st.button("Generate Quote"):
    with st.spinner("Generating quote..."):
        try:
            response = st.session_state.model.chat(
                user_message, system_prompt, max_new_tokens=max_tokens
            )
            st.success("Quote generated!")
            st.text_area("Generated Quote", response, height=200)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Powered by Llama3QuoteModel, Ollama, and Streamlit.")
