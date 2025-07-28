import warnings

def test_imports() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_openai import OpenAIEmbeddings
        from langchain_community.document_loaders import TextLoader
        from langchain.memory import ConversationBufferMemory


