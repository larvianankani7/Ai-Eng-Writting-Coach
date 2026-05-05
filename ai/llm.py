from langchain_community.llms import Ollama
def get_llm():
    llm = Ollama(model="llama3")
    return llm
