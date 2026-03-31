"""
QA Agent
Focuses entirely on QA generation with strict citation enforcement using RAG.
"""

import time
import yaml
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

from rag_engine import RAGEngine
from data_models import Evidence

def load_prompt(prompt_name: str, config_path: str = "prompts.yaml") -> str:
    """Load prompt from central YAML configuration"""
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            return config.get('system_prompts', {}).get(prompt_name, "")
    except Exception as e:
        print(f"Error loading prompt {prompt_name}: {e}")
        return ""

class AskMyDocsAgent:
    """Agent specialized in answering queries over domain documents"""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.1,
        verbose: bool = True
    ):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.verbose = verbose

        # Initialize Free Local LLM via Ollama
        # Note: You must have Ollama installed and running `ollama run llama3.2` or `mistral` locally
        # for this to work. It connects to the default local port 11434 automatically.
        # We override the model string to point to the local instance.
        self_model = "llama3.2" if model == "gpt-4o-mini" else model
        
        self.llm = ChatOllama(
            model=self_model,
            temperature=temperature
        )
        
        self.system_prompt_template = load_prompt('qa_agent')
        if not self.system_prompt_template:
            # Fallback if config isn't found
            self.system_prompt_template = (
                "You are a strict QA assistant. Answer only using the provided context.\n"
                "If the answer is not in the context, say 'I cannot answer this question based on the provided documents.'\n"
                "Always cite sources like [Source: filename].\n\nContext:\n{context}"
            )

    def format_evidence_for_prompt(self, evidence_list: List[Evidence]) -> str:
        """Format retrieved evidence for the LLM context"""
        formatted = []
        for i, e in enumerate(evidence_list, 1):
            source = e.source_file
            content = e.content.strip()
            formatted.append(f"--- Document {i} [Source: {source}] ---\n{content}\n")
            
        return "\n".join(formatted)

    def answer_query(
        self,
        query: str,
        rag_engine: RAGEngine,
        top_k: int = 5
    ) -> Tuple[str, List[Evidence], float]:
        """
        Retrieves evidence and generates an answer, strictly declining if unsupported.
        """
        start_time = time.time()
        
        if self.verbose:
            print("\n" + "="*70)
            print(f"🤖 QA AGENT - Query: {query}")
            print("="*70)
            
        # 1. Retrieve evidence using hybrid search & cross-encoder
        evidence_list = rag_engine.retrieve_evidence(
            query=query,
            k=top_k,
            enhance_query=True
        )
        
        # 2. Format evidence (will be empty string if no evidence)
        context_text = self.format_evidence_for_prompt(evidence_list) if evidence_list else "No documents matched the query."
        
        # 3. Build Prompt
        system_prompt = self.system_prompt_template.format(context=context_text)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Question: {query}")
        ]
        
        if self.verbose:
            print(f"🧠 Generating response using {len(evidence_list)} evidence chunks...")
            
        # 4. Generate Answer
        response = self.llm.invoke(messages)
        answer = response.content
        
        execution_time = time.time() - start_time
        
        if self.verbose:
            print(f"✅ Generated answer ({len(answer)} chars)")
            print(f"⏱️ Time: {execution_time:.2f}s")
            print("="*70)
            
        return answer, evidence_list, execution_time
