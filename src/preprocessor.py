# src/preprocessor.py

import re
from typing import List, Dict

import spacy

# Charge le pipeline français de spaCy
nlp = spacy.load("fr_core_news_sm")


def normalize_text(text: str) -> str:
    text = text.replace("\xa0", " ").replace("\t", " ")
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[ ]{2,}", " ", text)
    return text.strip()


def segment_paragraphs(text: str) -> List[str]:
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def segment_sentences(text: str) -> List[str]:
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents if sent.text.strip()]


def chunk_sentences(sentences: List[str], max_chars: int = 1000) -> List[str]:
    chunks, current = [], ""
    for sent in sentences:
        if len(current) + len(sent) + 1 <= max_chars:
            current = (current + " " + sent).strip()
        else:
            if current:
                chunks.append(current)
            current = sent
    if current:
        chunks.append(current)
    return chunks


def preprocess_entries(entries: List[Dict]) -> List[Dict]:
    processed = []
    for e in entries:
        text = normalize_text(e["text"])
        for para in segment_paragraphs(text):
            sents = segment_sentences(para)
            for chunk in chunk_sentences(sents, max_chars=1000):
                processed.append(
                    {"date": e["date"], "text": chunk, "source": e["filename"]}
                )
    return processed
