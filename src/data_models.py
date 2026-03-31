"""
Data Models for Ask My Docs
Using Pydantic for validation and type safety
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Evidence(BaseModel):
    """Evidence from RAG retrieval"""
    source_file: str
    doc_type: str  # e.g., 'rfp', 'proposal', 'markdown', 'web'
    content: str
    similarity_score: float
    metadata: Dict[str, Any] = Field(default_factory=dict)
    retrieval_timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
