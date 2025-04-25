# src/test_indexer.py

import os, sys

here = os.path.dirname(__file__)
sys.path.insert(0, here)

from loader import load_journal
from preprocessor import preprocess_entries
from indexer import build_vectorstore

if __name__ == "__main__":
    # 1) Charge et prétraite
    journal_dir = os.path.abspath(os.path.join(here, "..", "data", "journal"))
    entries = load_journal(journal_dir)
    processed = preprocess_entries(entries)

    # 2) Indexe
    vectordb = build_vectorstore(
        processed, persist_directory=os.path.abspath("db/chroma")
    )
    print("✅ Vectorstore créé dans db/chroma")

    # 3) Test de recherche sémantique
    query = "compétence intelligence artificielle"
    results = vectordb.similarity_search(query, k=3)
    print(f"\nTop 3 résultats pour '{query}':\n")
    for doc in results:
        print(
            "–", doc.metadata, "\n ", doc.page_content[:200].replace("\n", " "), "…\n"
        )
