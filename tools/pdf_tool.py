# tools/pdf_tool.py
# PDF RAG tool builder — ingests PDF, stores in FAISS, returns LangChain retriever tool.

import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.tools.retriever import create_retriever_tool

EMBED_MODEL = "all-MiniLM-L6-v2"
VECTOR_PATH = str(Path(__file__).parent.parent / "vectorstore" / "faiss_index")


def build_pdf_tool(pdf_path: str):
    """
    Ingest a PDF, embed chunks into FAISS, return a LangChain retriever tool.
    If FAISS index already exists it merges new chunks in.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    if os.path.exists(VECTOR_PATH) and os.listdir(VECTOR_PATH):
        vs = FAISS.load_local(VECTOR_PATH, embeddings, allow_dangerous_deserialization=True)
        vs.add_documents(chunks)
    else:
        vs = FAISS.from_documents(chunks, embeddings)

    vs.save_local(VECTOR_PATH)

    retriever = vs.as_retriever(search_kwargs={"k": 4})

    return create_retriever_tool(
        retriever,
        name="pdf_search",
        description=(
            "Use this tool FIRST whenever the question is related to the uploaded PDF document. "
            "Always prefer this over web tools for questions about the uploaded file."
        ),
    )


def load_existing_pdf_tool():
    """Load an already-saved FAISS index as a retriever tool (no re-ingestion)."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = FAISS.load_local(VECTOR_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = vs.as_retriever(search_kwargs={"k": 4})
    return create_retriever_tool(
        retriever,
        name="pdf_search",
        description="Use this tool FIRST for questions about the uploaded PDF document.",
    )