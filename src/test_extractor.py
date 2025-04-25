# src/test_extractor.py

import os, sys

here = os.path.dirname(__file__)
sys.path.insert(0, here)

from loader import load_journal
from preprocessor import preprocess_entries
from extractor import annotate_chunks_with_entities

if __name__ == "__main__":
    journal_dir = os.path.abspath(os.path.join(here, "..", "data", "journal"))
    entries = load_journal(journal_dir)
    chunks = preprocess_entries(entries)
    annotated = annotate_chunks_with_entities(chunks[:5])  # test sur 5 premiers

    for idx, a in enumerate(annotated):
        print(f"── Chunk {idx+1} ({a['source']} – {a['date'].date()}):")
        print("Texte brut :", a["text"][:100].replace("\n", " "), "…")
        print("SpaCy ents:", a["spacy_ents"])
        print("PII Presidio:", [(r.entity_type, r.start, r.end) for r in a["pii"]])
        print("Texte anonymisé :", a["anonymized"][:100].replace("\n", " "), "…\n")
