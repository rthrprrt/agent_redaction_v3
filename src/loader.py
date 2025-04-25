import os
import re
from datetime import datetime
from typing import List, Dict

from docx import Document


def parse_date_from_filename(filename: str) -> datetime:
    """
    Extrait la date depuis un nom de fichier au format 'YYYY-MM-DD*.docx'.
    Ajuste la regex si ton format diffère.
    """
    match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
    if not match:
        raise ValueError(f"Impossible d'extraire une date depuis '{filename}'")
    return datetime.fromisoformat(match.group(1))


def load_journal(directory: str) -> List[Dict]:
    """
    Parcourt tous les .docx du dossier et retourne une liste de dicts :
    [
      { 'date': datetime, 'text': '...' },
      ...
    ]
    """
    entries = []
    for fname in sorted(os.listdir(directory)):
        if not fname.lower().endswith(".docx"):
            continue
        path = os.path.join(directory, fname)
        # 1) Extraire la date
        date = parse_date_from_filename(fname)
        # 2) Lire le document
        doc = Document(path)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        text = "\n\n".join(paragraphs)
        entries.append({"date": date, "text": text, "filename": fname})
    return entries


if __name__ == "__main__":
    # test rapide
    import pprint

    journal_dir = os.path.join(os.path.dirname(__file__), "..", "data", "journal")
    journal_dir = os.path.abspath(journal_dir)
    entries = load_journal(journal_dir)
    print(f"Chargés {len(entries)} fichiers depuis {journal_dir}")
    pprint.pprint(entries[:2])
