import os
from llama_index.core import VectorStoreIndex, load_index_from_storage
from llama_index.core.storage import StorageContext
from pypdf import PdfReader


def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print("building index", index_name)
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=index_name)
        )

    return index

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

pdf_path = os.path.join("data", "Canada.pdf")
canada_pdf = read_pdf(pdf_path)
canada_index = get_index(canada_pdf, "canada")
canada_engine = canada_index.as_query_engine()
