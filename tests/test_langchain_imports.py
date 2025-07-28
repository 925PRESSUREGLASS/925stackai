from importlib import import_module


def test_import_paths() -> None:
    assert import_module("langchain_huggingface")
    assert import_module("langchain_openai")
    assert import_module("langchain_community")
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain_community.document_loaders import CSVLoader
    from langchain.memory import ConversationBufferMemory

    assert HuggingFaceEmbeddings
    assert OpenAIEmbeddings
    assert ChatOpenAI
    assert CSVLoader
    assert ConversationBufferMemory
