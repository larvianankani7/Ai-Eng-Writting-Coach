from processing.cleaner import clean_text
from processing.splitter import split_text
def process_text(text: str):
    cleaned = clean_text(text)
    chunks = split_text(cleaned)
    return chunks