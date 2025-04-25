# src/test_preprocessor.py

import os, sys

here = os.path.dirname(__file__)
sys.path.insert(0, here)

from loader import load_journal
from preprocessor import preprocess_entries

if __name__ == "__main__":
    journal_dir = os.path.abspath(os.path.join(here, "..", "data", "journal"))
    entries = load_journal(journal_dir)
    processed = preprocess_entries(entries)
    print(f"{len(entries)} journaux → {len(processed)} chunks prêts à indexer\n")
    for chunk in processed[:3]:
        print("──", chunk["date"].date(), chunk["source"])
        print(chunk["text"][:200].replace("\n", " "), "…\n")
