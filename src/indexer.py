# src/indexer.py

import os
from typing import List, Dict
import torch

# Imports mis à jour pour éviter les dépréciations
try:
    from langchain_community.embeddings import SentenceTransformerEmbeddings
    from langchain_community.vectorstores import FAISS
except ImportError:
    from langchain.embeddings import SentenceTransformerEmbeddings
    from langchain.vectorstores import FAISS


def build_vectorstore(
    processed: List[Dict],
    persist_directory: str = None,  # on accepte désormais ce paramètre
) -> FAISS:
    """
    Construit un FAISS vectorstore en mémoire à partir des chunks.
    Le paramètre persist_directory est ignoré ici (FAISS n'est pas persistant).
    """
    # Détection automatique du device (CPU si pas de CUDA)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    embeddings = SentenceTransformerEmbeddings(
        model_name="paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": device},
    )

    texts = [e["text"] for e in processed]
    metadatas = [
        {"date": e["date"].isoformat(), "source": e["source"]} for e in processed
    ]

    vectordb = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
    return vectordb
