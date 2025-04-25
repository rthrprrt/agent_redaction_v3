# src/extractor.py

import os
from typing import List, Dict

import spacy
from presidio_analyzer import AnalyzerEngine, RecognizerResult
from presidio_anonymizer import AnonymizerEngine

# Charge spaCy fr pour la segmentation et NER
nlp = spacy.load("fr_core_news_sm")

# Configure Presidio pour détecter et anonymiser les PII
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


def extract_spacy_entities(text: str) -> List[Dict]:
    """
    Repère les entités via spaCy (PERSON, ORG, etc.).
    """
    doc = nlp(text)
    return [
        {
            "label": ent.label_,
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char,
        }
        for ent in doc.ents
    ]


def extract_pii_via_presidio(text: str) -> List[RecognizerResult]:
    """
    Tente de détecter les PII (PERSON, LOCATION, EMAIL_ADDRESS, PHONE_NUMBER)
    via Presidio Analyzer. Si aucun recognizer n'est disponible, renvoie [].
    """
    try:
        results = analyzer.analyze(
            text=text,
            entities=["PERSON", "LOCATION", "EMAIL_ADDRESS", "PHONE_NUMBER"],
            language="fr",
        )
        return results
    except ValueError:
        # Pas de recognizers configurés pour la langue, on renvoie vide
        return []


def anonymize_text(text: str) -> str:
    """
    Anonymise les PII détectées avec la configuration par défaut
    (remplacement par le nom de l'entité). Si pas de PII, renvoie le texte inchangé.
    """
    results = extract_pii_via_presidio(text)
    if not results:
        return text

    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized.text


def annotate_chunks_with_entities(chunks: List[Dict]) -> List[Dict]:
    """
    Pour chaque chunk {'date', 'text', 'source'}, ajoute :
      - 'spacy_ents': entités spaCy
      - 'pii': résultats Presidio Analyzer (éventuellement [])
      - 'anonymized': texte anonymisé ou original
    """
    annotated = []
    for c in chunks:
        text = c["text"]
        spacy_ents = extract_spacy_entities(text)
        pii = extract_pii_via_presidio(text)
        anonymized = anonymize_text(text)
        annotated.append(
            {
                **c,
                "spacy_ents": spacy_ents,
                "pii": pii,
                "anonymized": anonymized,
            }
        )
    return annotated
