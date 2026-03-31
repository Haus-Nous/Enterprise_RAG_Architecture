import sys
import os
from pathlib import Path
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

# Add src to path so we can import our RAG engine
sys.path.insert(0, str(Path.cwd() / 'src'))

from dotenv import load_dotenv
load_dotenv()

from rag_engine import RAGEngine
from qa_agent import AskMyDocsAgent

app = FastAPI(
    title="Ask My Docs API",
    description="Production RAG API with Hybrid Retrieval and Citations",
    version="1.0.0"
)

# Allow React frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # React default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances (lazy loaded)
rag_engine = None
qa_agent = None

def get_rag_engine():
    global rag_engine
    if rag_engine is None:
        # No API key required for free local huggingface embeddings!
        api_key = os.getenv('OPENAI_API_KEY', "optional_local_key")
        rag_engine = RAGEngine(api_key=api_key, verbose=True)
    return rag_engine

def get_qa_agent():
    global qa_agent
    if qa_agent is None:
        # No API key required for free local Ollama generation!
        api_key = os.getenv('OPENAI_API_KEY', "optional_local_key")
        qa_agent = AskMyDocsAgent(api_key=api_key, verbose=True)
    return qa_agent


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5

class EvidenceResponse(BaseModel):
    source_file: str
    content: str
    similarity_score: float

class ChatResponse(BaseModel):
    answer: str
    evidence: List[EvidenceResponse]
    execution_time_seconds: float


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Ask My Docs API is running"}


@app.post("/api/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    """
    Handles a user query by retrieving context and generating a cited response.
    """
    try:
        rag = get_rag_engine()
        agent = get_qa_agent()
        
        answer_text, evidence_list, exec_time = agent.answer_query(
            query=request.query,
            rag_engine=rag,
            top_k=request.top_k
        )
        
        # Format evidence for the frontend
        formatted_evidence = [
            {
                "source_file": e.source_file,
                "content": e.content,
                "similarity_score": e.similarity_score
            }
            for e in evidence_list
        ]
        
        return {
            "answer": answer_text,
            "evidence": formatted_evidence,
            "execution_time_seconds": exec_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/index")
def reindex_database():
    """
    Forces a complete re-index of the document database.
    """
    try:
        rag = get_rag_engine()
        rag.clear_collection()
        results = rag.index_documents()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Receives and saves a document to the correct local directory.
    """
    try:
        # Determine the target directory based on file extension
        ext = Path(file.filename).suffix.lower()
        
        if ext == '.pdf':
            target_dir = Path.cwd() / 'data' / 'rfps'
        elif ext == '.md':
            target_dir = Path.cwd() / 'data' / 'markdown'
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}. Please upload a .pdf or .md file.")
            
        # Ensure the target directory exists
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Build the final file path
        file_path = target_dir / file.filename
        
        # Save the file out to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"status": "success", "filename": file.filename, "message": "File uploaded successfully."}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
