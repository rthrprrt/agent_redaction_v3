# Agent de rédaction autonome

## To-do list

### Phase 0 – Initialisation et infrastructure
1. **Configurer l’environnement local** – ✔️
2. **Tester Llama 3.1 Q8 via Ollama** – ✔️
3. **Structurer dépôt Git & CI légère** – ✔️

### Phase 1 – Ingestion et indexation
4. **Module d’ingestion DOCX** – ✔️
5. **Prétraitement et segmentation** – ✔️
6. **Indexation vectorielle (FAISS)** – ✔️

### Phase 2 – Extraction & planification
7. **Pipeline NLP extraction & anonymisation** – ✔️
8. **Résumé itératif & raffinement** – ◻️
9. **Génération de l’ossature (plan)** – ◻️

### Phase 3 – Rédaction & feedback
10. **Rédaction section par section** – ◻️
11. **Interface de feedback minimal** – ◻️
12. **Tests d’intégration et évaluation** – ◻️

## Progrès actuel

- Modules `loader.py`, `preprocessor.py`, `indexer.py`, `extractor.py` implémentés et testés.
- Environnement local configuré (Python, venv, Git, pre-commit).
- Modèle Llama 3.1 Q8 opérationnel via Ollama.
- Data ingestion, nettoyage, segmentation, indexation RAG et extraction d’entités fonctionnels.

## Étapes suivantes

1. Implémenter la **Résumé itératif & raffinement** via LangChain RefineChain.
2. Générer automatiquement l’**ossature du rapport** (plan détaillé).
3. Développer la **rédaction progressive** des sections.
4. Mettre en place l’**interface de feedback** (CLI/notebook ou web).
5. Réaliser les **tests d’intégration** et ajuster les prompts.
6. (Optionnel) Ajouter UI web (Streamlit / FastAPI + React).
7. Documenter le pipeline et préparer la soutenance.

```mermaid
graph TD
    subgraph "📚 Knowledge Ingestion"
        A[Journal DOCX] --> B[loader.py]
        B --> C[preprocessor.py]
        C --> D[Text Chunks]
    end
    
    subgraph "🧠 Agent Memory"
        D --> E[indexer.py]
        D --> F[extractor.py]
        E --> G[Vector Memory<br/>FAISS + Embeddings]
        F --> H[Entity Memory<br/>NER + PII Detection]
    end
    
    subgraph "🤖 AI Agent Core"
        I[Ollama LLM<br/>llama3.1:8b] --> J[Reasoning Engine]
        G -->|Retrieval| J
        H -->|Context| J
        J --> K[Report Generation]
    end
    
    subgraph "📝 Agent Output"
        K --> L[Structured Report]
        L --> M[Final Document]
    end
    
    subgraph "🔧 Agent Tools"
        N[SpaCy NLP] --> F
        O[Presidio Privacy] --> F
        P[SentenceTransformers] --> E
        Q[LangChain RAG] --> J
    end
    
    subgraph "🧪 Agent Testing"
        R[test_*.py] -.-> B
        R -.-> C
        R -.-> E
        R -.-> F
        R -.-> I
    end
    
    style I fill:#ff9800
    style J fill:#ff9800
    style G fill:#2196f3
    style H fill:#9c27b0
    style M fill:#4caf50
    style A fill:#e3f2fd
```
