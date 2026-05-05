from langchain_community.document_loaders import PyPDFLoader
def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text = " ".join([doc.page_content for doc in docs])
    return text