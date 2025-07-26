from llama3_model.model import Llama3QuoteModel

if __name__ == "__main__":
    model = Llama3QuoteModel()
    response = model.chat(
        "How much would it cost to replace a window?",
        system_prompt="You are a helpful quoting assistant.",
    )
    print("Response:", response)
