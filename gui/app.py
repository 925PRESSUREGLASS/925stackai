import streamlit as st
from agents.quote_agent import run_quote
from .components import parse_quote_output, render_quote


def main() -> None:
    st.set_page_config(page_title="Quote Assistant", layout="wide")
    st.title("Quoting Assistant")

    if "history" not in st.session_state:
        st.session_state.history = []

    left, right = st.columns(2)

    with left:
        st.header("Chat History")
        for entry in st.session_state.history:
            st.write(f"**You:** {entry['prompt']}")
            st.write(f"**Total:** {entry['data'].get('total', 0)}")
        prompt = st.text_area("Describe the job", key="prompt_input")
        if st.button("Generate Quote"):
            if prompt.strip():
                output = run_quote(prompt.strip())
                data = parse_quote_output(output)
                st.session_state.history.append(
                    {"prompt": prompt.strip(), "data": data}
                )
                st.session_state.prompt_input = ""
                st.experimental_rerun()

    with right:
        st.header("Quote")
        if st.session_state.history:
            render_quote(st.session_state.history[-1]["data"])
        else:
            st.write("Enter a job description to generate a quote.")


if __name__ == "__main__":
    main()
