# 📸 Recruiter-Grade Documentation & Screenshot Asset Plan

This asset plan outlines the visual strategy for the **Enterprise RAG Architecture** repository. In high-level AI engineering hiring, recruiters and hiring managers spend an average of 30-40 seconds reviewing a GitHub repository. Rich, high-fidelity visual assets demonstrate that a project is a working, production-grade system rather than a code tutorial.

---

## 📂 Assets Directory Structure
The assets folder is structured within the project as follows:
```text
docs/
└── assets/
    ├── .gitkeep                 # Folder placeholder
    ├── 01_landing_page.png      # Initial dashboard state
    ├── 02_upload_workflow.png   # Document drop zone and loaders
    ├── 03_sync_index.png        # Re-indexing stats updates
    ├── 04_query_console.png     # Typing query & loading state
    ├── 05_cited_response.png    # Response formatting & inline citations
    ├── 06_citations_panel.png   # Expanded cross-encoder source accordion
    ├── 07_evaluation_logs.png   # Ragas quantitative metrics output
    ├── 08_architecture_v2.png   # Rendered inference architecture
    ├── demo_inference.gif       # GIF: End-to-End Q&A execution
    └── demo_sync.gif            # GIF: Document upload and indexing sync
```

---

## 📋 Screenshot Checklist & Technical Specifications

### 1. Landing Page
* **Title:** Initial Chat Dashboard State
* **What should be visible:**
  * Clean, dark-mode/modern UI layout (Vite/React).
  * Main chat area showing the empty state container: Lucide `Bot` icon, title "How can I help you today?", and description text.
  * Sidebar showing database status indicators ("Vector Semantic Search: active", "BM25 Keyword Search: active") and the "Re-Index Database" button.
* **Why it matters:** Establishes a professional first impression. It proves the app has a premium, responsive interface and is ready for interaction.
* **README Caption:** `Figure 1: Enterprise Knowledge Retrieval Dashboard featuring a modern dark-themed interactive UI and live database status indicators.`

### 2. Upload Workflow
* **Title:** Multi-Format Document Ingestion Zone
* **What should be visible:**
  * Sidebar drag-and-drop file upload zone.
  * A file (e.g., `Project_Aegis_Proposal.pptx` or `RFP_Requirements.pdf`) dragging over the active upload zone, changing color borders.
  * Successful upload status toast or message below the upload box.
* **Why it matters:** Visually demonstrates the ingestion layer's support for multiple file formats (especially complex PowerPoint slide decks and PDFs) without requiring raw terminal uploads.
* **README Caption:** `Figure 2: Multi-format document ingestion interface showing drag-and-drop PPTX slide deck upload.`

### 3. Re-indexing Workflow
* **Title:** Live Indexing Synchronization
* **What should be visible:**
  * The "Re-Index Database" button showing a spinning loader icon and text "Syncing...".
  * Sidebar counters incrementing in real-time under **Knowledge Base Stats**: "Documents: 4", "Embeddings: 148" (reflecting the `documents_processed` and `chunks_generated` JSON response).
* **Why it matters:** Shows that the index is fully dynamic. Adding a document triggers automated background re-indexing, recalculating dense vectors and updating the lexical BM25 index on the fly.
* **README Caption:** `Figure 3: Real-time background index synchronization for ChromaDB and BM25 search structures.`

### 4. Query Interface
* **Title:** RAG Query Validation & Loading State
* **What should be visible:**
  * Input textarea containing a domain-specific question (e.g., *"What is the steering committee meeting frequency for Project Aegis?"*).
  * Send button in active state.
  * A loading placeholder block in the message area showing the typing indicator animations along with the text: *"Running Hybrid Retrieval & Re-ranking..."*.
* **Why it matters:** Highlights the loading state UX and proves that the backend is working through retrieval and re-ranking pipelines before returning results.
* **README Caption:** `Figure 4: Active query input console executing a dense-sparse search request with background pipeline progress indicators.`

### 5. Generated Answer
* **Title:** Constrained Synthesized Response
* **What should be visible:**
  * The markdown response returned by Llama 3.2.
  * Response formatted with headers, bold text, and bullet points.
  * Multiple inline citation tags (e.g., `[Source: Project_Aegis_Proposal.pptx]`, `[Source: governance_rules.md]`) appended directly to factual statements.
  * A minor label at the bottom: *"Resolved in 1.48s"*.
* **Why it matters:** Proves the citation model works. Recruiters can see that the LLM is constrained to prevent hallucinations and strictly attributes facts to specific source files.
* **README Caption:** `Figure 5: Factually-grounded markdown response synthesized by local Llama 3.2, enforcing source references and displaying processing latency.`

### 6. Source Citations
* **Title:** Expanded Evidence Panel & Relevance Scores
* **What should be visible:**
  * The source citation accordion expanded below the answer, showing *"2 Sources Retrieved by Cross-Encoder"*.
  * Individual citation cards showing:
    * File type icon and source filename (e.g., `Project_Aegis_Proposal.pptx`).
    * Relevance match score (e.g., `89.2% Match`) calculated by the cross-encoder model.
    * The exact raw text chunk/slide snippet retrieved from the vector store.
* **Why it matters:** Highlights the system's auditability. It shows how the cross-encoder re-ranks text chunks to provide highly relevant context for generation.
* **README Caption:** `Figure 6: Expanded source citation panel showing raw retrieved text chunks and cross-encoder relevance scores.`

### 7. Evaluation Results
* **Title:** Quantitative Ragas Evaluation Metrics
* **What should be visible:**
  * A terminal screen or UI dashboard card showing the output logs of `./tests/run_evaluation.sh`.
  * The printed evaluation results summary in JSON:
    ```json
    {
        "faithfulness": 0.938,
        "answer_relevancy": 0.891,
        "context_precision": 0.884,
        "context_recall": 0.912
    }
    ```
* **Why it matters:** Demonstrates a metric-driven approach to AI development. It shows recruiters that you evaluate prompt and model updates quantitatively rather than relying on "vibes-based" manual checking.
* **README Caption:** `Figure 7: Offline RAGAS evaluation output showing quantitative scores for faithfulness, answer relevancy, and context precision.`

### 8. System Architecture
* **Title:** High-Fidelity RAG Architecture Schema
* **What should be visible:**
  * A clean visual export of the redesigned Mermaid.js architecture diagrams (Production Pipeline & Evaluation Pipeline).
* **Why it matters:** Provides an immediate mental model of how the system works, acting as a great talking point for system architecture interviews.
* **README Caption:** `Figure 8: High-fidelity system architecture diagrams showing production inference and offline Ragas evaluation pipelines.`

---

## 📹 Recommended GIF Demonstrations

Embedded GIFs capture immediate attention on a GitHub README. Below are the specifications for two recommended GIFs to record for this project:

### GIF 1: The End-to-End Q&A Cycle
* **Duration:** ~12-15 seconds.
* **Workflow to record:**
  1. Type a query: *"What is the steering committee frequency for Project Aegis?"*
  2. Click **Send** (watch the typing indicator active for ~1.5s).
  3. The markdown answer appears, displaying inline citations.
  4. Scroll down and click the **Sources accordion** to expand it.
  5. Hover over the source match badges showing `89.2% Match` to show interactivity.
* **Why it matters:** Quickly demonstrates the application's responsiveness, UI design, citations, and re-ranking capabilities.

### GIF 2: Document Ingestion & Synchronous Re-indexing
* **Duration:** ~8-10 seconds.
* **Workflow to record:**
  1. Drag a new PDF document (`Q4_Financials.pdf`) into the sidebar drop zone.
  2. Watch the upload complete successfully.
  3. Click **"Re-Index Database"** (button changes to "Syncing...").
  4. The sidebar database stats counters (Documents, Embeddings) increment live.
* **Why it matters:** Proves the system handles document ingestion and vectorization dynamically in the background without needing terminal commands.
