import importlib
import warnings


def test_imports() -> None:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        importlib.import_module("langchain_huggingface")
        from langchain_huggingface import HuggingFaceEmbeddings  # noqa: F401
        from langchain_openai import OpenAIEmbeddings  # noqa: F401
        from langchain_community.document_loaders import TextLoader  # noqa: F401
        from langchain.memory import ConversationBufferMemory  # noqa: F401
    assert not w
