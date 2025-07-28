import streamlit as st

from orchestrator import Orchestrator


st.title("925stackai – Quoting Demo (wire-up)")

user_prompt = st.text_input("Enter a prompt to quote:")

if st.button("Generate Quote") and user_prompt:
    orchestrator = Orchestrator()
    response = orchestrator.run(user_prompt)
    st.markdown("### Response")
    st.write(response)
