"""
Create Evaluation Dataset
Generates a "golden" dataset of QA pairs from the ingested documents using Ragas.
"""

import os
import json
from pathlib import Path
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from ragas.testset.generator import TestsetGenerator
from ragas.testset.evolutions import simple, reasoning, multi_context
from langchain_core.documents import Document

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

def load_documents_from_chroma(db_path: str = "data/chroma_db") -> list[Document]:
    """Load all chunks from the Chroma vector store to use as context for generation"""
    if not Path(db_path).exists():
        print(f"Error: Vector store not found at {db_path}")
        return []

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore = Chroma(
        collection_name="ask_my_docs_kb",
        embedding_function=embeddings,
        persist_directory=db_path
    )
    
    # Retrieve all documents
    db_items = vectorstore.get()
    
    docs = []
    if db_items and 'documents' in db_items and 'metadatas' in db_items:
        for text, meta in zip(db_items['documents'], db_items['metadatas']):
            docs.append(Document(page_content=text, metadata=meta))
            
    print(f"Loaded {len(docs)} document chunks from ChromaDB.")
    return docs

def generate_dataset(output_path: str = "tests/eval_dataset.json", num_questions: int = 15):
    """Generate the golden dataset using Ragas TestsetGenerator"""
    print(f"Generating {num_questions} evaluation Q&A pairs...")
    
    # Load Documents
    docs = load_documents_from_chroma()
    if not docs:
        print("No documents available for generation. Exiting.")
        return
        
    # Initialize Generator APIs
    generator_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    critic_llm = ChatOpenAI(model="gpt-4o", temperature=0.0) # Critic needs to be smart
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    # Configure Ragas Generator
    generator = TestsetGenerator.from_langchain(
        generator_llm,
        critic_llm,
        embeddings
    )
    
    # Define generation types
    distributions = {
        simple: 0.5,
        reasoning: 0.25,
        multi_context: 0.25
    }
    
    # Generate test set
    try:
        testset = generator.generate_with_langchain_docs(docs, test_size=num_questions, distributions=distributions)
        
        # Convert to pandas and then to dict for saving
        df = testset.to_pandas()
        
        # Clean up dataframe for our evaluation pipeline
        eval_data = []
        for _, row in df.iterrows():
            eval_data.append({
                "question": row["question"],
                "ground_truth": row["ground_truth"],
                "contexts": row["contexts"],
                "evolution_type": row["evolution_type"]
            })
            
        # Save to JSON
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(eval_data, f, indent=4)
            
        print(f"✅ Successfully generated and saved dataset to {output_path}")
        
    except Exception as e:
        print(f"Error generating dataset: {e}")

if __name__ == "__main__":
    generate_dataset(num_questions=10) # Keeping it to 10 for speed right now, scale up later.
