import os

from decouple import config
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

os.environ["GROQ_API_KEY"] = config("GROQ_API_KEY")
os.environ["HUGGINGFACE_API_KEY"] = config("HUGGINGFACE_API_KEY")

if __name__ == "__main__":
    file_path = "/app/rag/data/RagNiki.pdf"
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(docs)

    persist_directory = "app/chroma_data"
    os.makedirs(persist_directory, exist_ok=True)

    embedding = HuggingFaceEmbeddings()
    vector_store = Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory,
    )
    vector_store.add_documents(chunks)
