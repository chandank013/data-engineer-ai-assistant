# rag/ingest.py
# PDF ingestion pipeline: load -> split -> embed -> FAISS vector store.

import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

VECTOR_PATH = str(Path(__file__).parent.parent / "vectorstore" / "faiss_index")
EMBED_MODEL = "all-MiniLM-L6-v2"


def ingest_pdf(pdf_path: str) -> FAISS:
    """Load PDF, chunk it, embed with HuggingFace, save/merge to FAISS."""
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    emb = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    if os.path.exists(VECTOR_PATH) and os.listdir(VECTOR_PATH):
        vs = FAISS.load_local(VECTOR_PATH, emb, allow_dangerous_deserialization=True)
        vs.add_documents(chunks)
    else:
        vs = FAISS.from_documents(chunks, emb)

    vs.save_local(VECTOR_PATH)
    return vs


def load_vectorstore() -> FAISS:
    emb = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return FAISS.load_local(VECTOR_PATH, emb, allow_dangerous_deserialization=True)