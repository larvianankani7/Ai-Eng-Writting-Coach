import os
from langchain_community.document_loaders import WebBaseLoader
def load_web(url: str):
    os.environ["USER_AGENT"] = "Mozilla/5.0"
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs[0].page_content