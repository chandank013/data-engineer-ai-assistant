# rag/retriever.py
# Vector retriever builder for FAISS store.

from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

VECTOR_PATH = str(Path(__file__).parent.parent / "vectorstore" / "faiss_index")
EMBED_MODEL = "all-MiniLM-L6-v2"


def get_retriever(k: int = 4):
    """Return a FAISS retriever. Raises if index does not exist yet."""
    emb = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs = FAISS.load_local(VECTOR_PATH, emb, allow_dangerous_deserialization=True)
    return vs.as_retriever(search_kwargs={"k": k})