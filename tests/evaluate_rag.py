"""
Evaluate RAG Pipeline
Runs offline evaluation on the Ask My Docs system using Ragas metrics.
Assesses Answer Relevancy, Faithfulness, Context Precision, and Context Recall.
"""

import os
import json
import pandas as pd
from pathlib import Path
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

# Project specific imports (assumes run from root)
from src.rag_engine import RAGEngine
from src.qa_agent import AskMyDocsAgent

def load_dataset(dataset_path: str = "tests/eval_dataset.json"):
    """Load the golden evaluation dataset"""
    if not Path(dataset_path).exists():
        print(f"Error: Dataset not found at {dataset_path}")
        return None
        
    with open(dataset_path, "r") as f:
        data = json.load(f)
        return data

def run_evaluation(dataset_path: str = "tests/eval_dataset.json", output_path: str = "tests/eval_results.json"):
    """Run Ragas evaluation on the QA Agent against the dataset"""
    
    # 1. Initialize RAG and QA Agent
    print("Initializing Ask My Docs system...")
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not set.")
        return
        
    rag_engine = RAGEngine(api_key=api_key, verbose=False)
    qa_agent = AskMyDocsAgent(api_key=api_key, verbose=False)
    
    # 2. Load dataset
    raw_data = load_dataset(dataset_path)
    if not raw_data:
        return
        
    print(f"Loaded {len(raw_data)} questions for evaluation.")
    
    # 3. Generate answers
    eval_inputs = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": []
    }
    
    print("Generating answers using QA Agent and Hybrid RAG...")
    for item in raw_data:
        question = item["question"]
        ground_truth = item["ground_truth"]
        
        # Run through our pipeline
        answer, evidence, _ = qa_agent.answer_query(question, rag_engine, top_k=5)
        
        # Compile response contexts specifically as a list of strings for Ragas
        retrieved_contexts = [e.content for e in evidence]
        
        eval_inputs["question"].append(question)
        eval_inputs["answer"].append(answer)
        eval_inputs["contexts"].append(retrieved_contexts)
        eval_inputs["ground_truth"].append(ground_truth)
        
    # 4. Evaluate using Ragas
    print("Running Ragas evaluation metrics (Faithfulness, Relevancy, Precision, Recall)...")
    dataset = Dataset.from_dict(eval_inputs)
    
    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ]
    
    # Needs OPENAI_API_KEY in environment
    results = evaluate(
        dataset,
        metrics=metrics,
        raise_exceptions=False
    )
    
    # 5. Output and Save
    print("\n--- Evaluation Results ---")
    df = results.to_pandas()
    
    summary = {
        "faithfulness": df["faithfulness"].mean() if "faithfulness" in df else 0.0,
        "answer_relevancy": df["answer_relevancy"].mean() if "answer_relevancy" in df else 0.0,
        "context_precision": df["context_precision"].mean() if "context_precision" in df else 0.0,
        "context_recall": df["context_recall"].mean() if "context_recall" in df else 0.0,
    }
    
    print(json.dumps(summary, indent=4))
    
    # Save detailed
    df.to_json(output_path, orient='records', indent=4)
    print(f"✅ Saved detailed evaluation results to {output_path}")

    return summary
    
if __name__ == "__main__":
    run_evaluation()
