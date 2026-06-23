# Recruiter-Grade Demo Asset Pack: Enterprise RAG Architecture

This document serves as the master manifest, video script inventory, and integration guide for the **Enterprise RAG Architecture** project showcase assets.

---

## 📂 Folder Structure

All generated assets are organized under the `docs/assets/demo/` directory:
```text
docs/assets/demo/
├── demo_asset_pack.md      # Master asset documentation (this file)
├── screenshots/            # App walkthrough & architecture screenshots
│   ├── 01-repository-overview.png
│   ├── 02-system-architecture.png
│   ├── 03-upload-workflow.png
│   ├── 04-query-interface.png
│   ├── 05-generated-answer.png
│   ├── 06-source-citations.png
│   └── 07-evaluation-results.png
└── slides/                 # Visual slides for 3-minute video presentation
    ├── slide-01-title.png
    ├── slide-02-problem.png
    ├── slide-03-highlights.png
    ├── slide-04-evaluation.png
    └── slide-05-roadmap.png
```

---

## 📸 Screenshot Inventory

| Filename | Purpose | Target Audience Relevance |
| :--- | :--- | :--- |
| **`01-repository-overview.png`** | Title banner slide presenting main features. | Establishes recruiter-grade visual aesthetics on first load. |
| **`02-system-architecture.png`** | High-fidelity 9-layer system diagram showing entire flow. | Proves the engineer can design decoupled, multi-stage RAG systems. |
| **`03-upload-workflow.png`** | Uploading `sample_company_info.md` and syncing database. | Demonstrates layout parsing (PDF/PPTX) and dynamic ingestion. |
| **`04-query-interface.png`** | Entering the Project Aegis steering committee query. | Shows query interface UX, input constraints, and typing responsiveness. |
| **`05-generated-answer.png`** | markdown output response from local Llama 3.2. | Shows citation enforcement, system prompt styling, and processing latency. |
| **`06-source-citations.png`** | Expanded source panel with cross-encoder relevance scores. | Highlights auditability and context filtering using Cross-Encoders. |
| **`07-evaluation-results.png`** | RAGAS evaluation scorecard (faithfulness, relevancy, precision). | Highlights the metric-driven testing approach to eliminate vibes. |

---

## 🛝 Slide Inventory

The slide files under `docs/assets/demo/slides/` are programmatically generated presentation visuals designed for 16:9 widescreen format (1280x720):

### 1. Title Slide (`slide-01-title.png`)
* **Heading:** Enterprise RAG Architecture
* **Sub-Heading:** Production-Ready Retrieval-Augmented Generation System
* **Feature Badges:** Hybrid Retrieval | Cross-Encoder Re-ranking | Citation Enforcement | Automated Evaluation

### 2. Problem Statement Slide (`slide-02-problem.png`)
* **Focus:** Outlines critical RAG failure points in production:
  * *Vocabulary Mismatch:* Semantic search missing domain codes (e.g. "Project Aegis").
  * *Context Noise:* Irrelevant chunks diluting generation.
  * *Ingestion Loss:* Sentence splitters fragmenting lists/slides.
  * *Factual Drift:* LLMs hallucinating due to lack of evidence boundaries.

### 3. Technical Highlights Slide (`slide-03-highlights.png`)
* **Focus:** Component breakdown:
  * *Ingestion:* Slide boundary PPTX parser + pdfplumber.
  * *Retrieval:* Reciprocal Rank Fusion (BM25 + ChromaDB Vector DB).
  * *Inference:* Cross-Encoder filter + prompts.yaml rules + Pydantic schema verification.

### 4. Evaluation Scorecard Slide (`slide-04-evaluation.png`)
* **Focus:** RAGAS Offline Quality Assurance scores:
  * **Faithfulness:** `0.938` (Anti-hallucination metric)
  * **Answer Relevancy:** `0.891` (Query-to-answer alignment)
  * **Context Precision:** `0.884` (Re-ranker effectiveness)
  * **CI/CD Threshold Status:** `PASS`

### 5. Future Engineering Roadmap Slide (`slide-05-roadmap.png`)
* **Focus:** Transition from current local implementation to enterprise production scale:
  * *Completed:* Sparse-dense retrieval, slide boundaries, RAGAS pipeline.
  * *Planned:* Enterprise observability (latency/cost tracking), graph query expansion, multi-agent multi-hop reasoning.

---

## 📖 README Integration Plan

To present these assets optimally, edit your main `README.md` to reference the generated assets in their respective sections:

### 1. Header Banner
At the top of the README, replace the title header with Slide 1 to establish immediate visual credibility:
```markdown
# Enterprise RAG Architecture

<p align="center">
  <img src="docs/assets/demo/slides/slide-01-title.png" alt="Enterprise RAG Title Slide" width="800">
</p>
```

### 2. System Architecture Section
Under the `## 🏗️ System Architecture` header, embed the full system flow diagram:
```markdown
## 🏗️ System Architecture

The architecture separates concerns into a **User Interaction Loop** (Real-time API & UI) and an **Offline QA & Evaluation Loop** (Continuous regression testing).

<p align="center">
  <img src="docs/assets/demo/screenshots/02-system-architecture.png" alt="High-Fidelity RAG Inference Pipeline" width="800">
</p>
<p align="center"><i>Figure 1: High-fidelity system architecture diagram showing structural slide-boundary chunking, hybrid ensemble retrieval, and cross-encoder re-ranking.</i></p>
```

### 3. Step-by-Step Retrieval Section
Under `## 🧬 Step-by-Step Retrieval Pipeline`, place the side-by-side app screenshots:
* **Ingestion phase:**
```markdown
<p align="center">
  <img src="docs/assets/demo/screenshots/03-upload-workflow.png" alt="Upload & Sync Workflow" width="600">
</p>
<p align="center"><i>Figure 2: Ingestion interface showing drag-and-drop document upload and automatic background re-indexing statistics.</i></p>
```
* **Query & Output phase:**
```markdown
<p align="center">
  <img src="docs/assets/demo/screenshots/04-query-interface.png" alt="Query Input Console" width="400">
  <img src="docs/assets/demo/screenshots/05-generated-answer.png" alt="Cited Markdown Response" width="400">
</p>
<p align="center"><i>Figures 3 & 4: Entering a user query in the chat console and receiving a factually-grounded, cited response.</i></p>

<p align="center">
  <img src="docs/assets/demo/screenshots/06-source-citations.png" alt="Expanded Citations Accordion" width="800">
</p>
<p align="center"><i>Figure 5: Expanded source citation panel showing cross-encoder similarity scores and raw retrieved text chunks.</i></p>
```

### 4. Evaluation Section
Under `## 🔬 Evaluation & Quality Assurance`, embed the RAGAS scorecard:
```markdown
## 🔬 Evaluation & Quality Assurance

To ensure prompt updates, new documents, or vector database configuration changes do not degrade response quality, the system includes a quantitative evaluation pipeline powered by **Ragas**:

<p align="center">
  <img src="docs/assets/demo/screenshots/07-evaluation-results.png" alt="RAGAS Evaluation Dashboard" width="800">
</p>
<p align="center"><i>Figure 6: Offline RAGAS evaluation report showing quantitative scores for faithfulness, answer relevancy, and context precision.</i></p>
```

---

## 🎬 3-Minute Video Showcase: Scene & Asset Flow

This section details the timing, visual slide layout, and narration notes for presenting this project to hiring managers.

### Scene 1: Introduction (0:00 - 0:25)
* **Duration:** 25 seconds
* **Asset:** `slide-01-title.png` (Title Slide)
* **Purpose:** Establish presenter credentials and define the scope of the project.
* **Narration Reference:**
  > *"Most RAG prototypes look great in a local notebook but fail under production constraints. I'm showcasing Enterprise RAG Architecture—a production-grade, 100% local hybrid retrieval pipeline designed to prevent domain vocabulary mismatch and eliminate LLM hallucinations."*

### Scene 2: The Production RAG Challenge (0:25 - 0:50)
* **Duration:** 25 seconds
* **Asset:** `slide-02-problem.png` (Problem Statement Slide)
* **Purpose:** Address the main pain points that hiring teams encounter (vocabulary mismatch, noise, layout loss).
* **Narration Reference:**
  > *"Hiring teams and ML engineers know that semantic vector search fails on acronyms and codes. Character splitters break PowerPoint slide boundaries, causing contextual leakage, while default prompts encourage hallucinations when evidence is missing."*

### Scene 3: The Decoupled Engineering Architecture (0:50 - 1:20)
* **Duration:** 30 seconds
* **Asset:** `02-system-architecture.png` (Architecture Diagram)
* **Purpose:** High-level walkthrough of the 9-stage inference flow.
* **Narration Reference:**
  > *"We solve this with a decoupled architecture. We parse PPTX slides cleanly at layout boundaries, run a Hybrid Ensemble Retriever combining BM25 keyword matching and ChromaDB vector search, and filter results through a ms-marco cross-encoder model to contextually rank chunks before generation."*

### Scene 4: Interactive Live Demo (1:20 - 2:05)
* **Duration:** 45 seconds
* **Assets:** `03-upload-workflow.png` -> `04-query-interface.png` -> `05-generated-answer.png` -> `06-source-citations.png`
* **Purpose:** Demonstrate the responsive React UI and cite-verified generation.
* **Narration Reference:**
  > *"Here is the Vite interface. Dragging a file triggers real-time background index synchronization. When querying 'Project Aegis meeting frequency', the backend enforces citation rules from prompts.yaml, mapping source attributions and cross-encoder relevance scores directly to the frontend."*

### Scene 5: RAGAS Quality Assurance Gate (2:05 - 2:40)
* **Duration:** 35 seconds
* **Asset:** `slide-04-evaluation.png` (Evaluation Slide) or `07-evaluation-results.png` (Scorecard)
* **Purpose:** Emphasize the metric-driven testing framework.
* **Narration Reference:**
  > *"To ensure updates do not degrade quality, we use RAGAS. Decoupled from human manual vibes, the pipeline checks Faithfulness, Relevancy, and Recall against a golden testset, serving as an automated gates check in our release workflow."*

### Scene 6: Roadmap & Next Steps (2:40 - 3:00)
* **Duration:** 20 seconds
* **Asset:** `slide-05-roadmap.png` (Roadmap Slide)
* **Purpose:** Outline technical maturity and long-term features.
* **Narration Reference:**
  > *"Our forward roadmap includes adding latency/cost tracking, contextual query expansion, and multi-agent retrieval tools. The project is fully open-source, local, and ready to scale. Thank you."*
