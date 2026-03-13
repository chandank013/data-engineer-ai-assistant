# rag/embeddings.py
# Centralised embedding model initialisation.

from langchain_community.embeddings import HuggingFaceEmbeddings

_emb_instance = None


def get_embeddings(model_name: str = "all-MiniLM-L6-v2") -> HuggingFaceEmbeddings:
    """Return a cached HuggingFace embedding instance."""
    global _emb_instance
    if _emb_instance is None:
        _emb_instance = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _emb_instance