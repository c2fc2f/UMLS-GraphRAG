import json
import os
from pathlib import Path
from statistics import mean, median
from typing import Any


CURRENT_DIR: str = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR: str = os.path.join(CURRENT_DIR, "results")
BENCHMARK_FILE: str = os.path.join(CURRENT_DIR, "benchmark.json")

def load_benchmark(benchmark_path: str) -> Any:
    """Load the benchmark.json file"""
    with open(benchmark_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_results(results_dir: str, benchmark_path: str) -> dict[str, Any]:
    """Analyze native and RAG results"""
    
    # Load benchmark
    benchmark: Any = load_benchmark(benchmark_path)
    
    # Statistics
    native_correct: int = 0
    native_total: int = 0
    rag_correct: int = 0
    rag_total: int = 0
    
    # For RAG metrics
    rag_errors: list[int] = []
    rag_nodes: list[int] = []
    rag_edges: list[int] = []
    
    # Browse all datasets
    results_path = Path(results_dir)
    
    for dataset_dir in results_path.iterdir():
        if not dataset_dir.is_dir():
            continue
            
        dataset_name: str = dataset_dir.name
        
        if dataset_name not in benchmark:
            print(f"⚠️  Dataset '{dataset_name}' not found in benchmark.json")
            continue
        
        # Browse result files
        for result_file in dataset_dir.glob("*.json"):
            filename: str = result_file.name
            
            # Identify type (native or rag) and question
            if filename.startswith("native_"):
                question_name: str = filename[7:-5]  # Remove "native_" and ".json"
                result_type: str = "native"
            elif filename.startswith("rag_"):
                question_name: str = filename[4:-5]  # Remove "rag_" and ".json"
                result_type: str = "rag"
            else:
                continue
            
            # Check if question exists in benchmark
            if question_name not in benchmark[dataset_name]:
                print(f"⚠️  Question '{question_name}' not found in benchmark[{dataset_name}]")
                continue
            
            # Load result
            with open(result_file, 'r', encoding='utf-8') as f:
                result: Any = json.load(f)
            
            # Get correct answer
            correct_answer: str = benchmark[dataset_name][question_name]["answer"]
            user_response: str = result.get("response")
            
            # Count results
            if result_type == "native":
                native_total += 1
                if user_response == correct_answer:
                    native_correct += 1
            else:  # rag
                rag_total += 1
                if user_response == correct_answer:
                    rag_correct += 1
                
                # Collect RAG metrics
                rag_errors.append(result.get("error", 0))
                rag_nodes.append(result.get("nodes", 0))
                rag_edges.append(result.get("edges", 0))
    
    # Calculate accuracy rates
    native_accuracy: float = (native_correct / native_total * 100) if native_total > 0 else 0
    rag_accuracy: float = (rag_correct / rag_total * 100) if rag_total > 0 else 0
    
    # Display results
    print("=" * 60)
    print("📊 ANALYSIS RESULTS")
    print("=" * 60)
    print()
    
    print("🔵 NATIVE")
    print(f"  ✓ Correct answers: {native_correct}/{native_total}")
    print(f"  📈 Accuracy rate: {native_accuracy:.2f}%")
    print()
    
    print("🟢 RAG")
    print(f"  ✓ Correct answers: {rag_correct}/{rag_total}")
    print(f"  📈 Accuracy rate: {rag_accuracy:.2f}%")
    print()
    
    if rag_errors:
        print("📉 RAG METRICS")
        print(f"  Errors     - Mean: {mean(rag_errors):.2f} | Median: {median(rag_errors):.2f}")
        print(f"  Nodes      - Mean: {mean(rag_nodes):.2f} | Median: {median(rag_nodes):.2f}")
        print(f"  Edges      - Mean: {mean(rag_edges):.2f} | Median: {median(rag_edges):.2f}")
    print()
    
    print("=" * 60)
    
    # Return results for programmatic use
    return {
        "native": {
            "correct": native_correct,
            "total": native_total,
            "accuracy": native_accuracy
        },
        "rag": {
            "correct": rag_correct,
            "total": rag_total,
            "accuracy": rag_accuracy,
            "metrics": {
                "errors": {"mean": mean(rag_errors) if rag_errors else 0, 
                          "median": median(rag_errors) if rag_errors else 0},
                "nodes": {"mean": mean(rag_nodes) if rag_nodes else 0, 
                         "median": median(rag_nodes) if rag_nodes else 0},
                "edges": {"mean": mean(rag_edges) if rag_edges else 0, 
                         "median": median(rag_edges) if rag_edges else 0}
            }
        }
    }

def main() -> None:
    # Check if files exist
    if not os.path.exists(RESULTS_DIR):
        print(f"❌ Error: Directory '{RESULTS_DIR}' does not exist")
        exit(1)
    
    if not os.path.exists(BENCHMARK_FILE):
        print(f"❌ Error: File '{BENCHMARK_FILE}' does not exist")
        exit(1)
    
    # Run analysis
    results: dict[str, Any] = analyze_results(RESULTS_DIR, BENCHMARK_FILE)

if __name__ == "__main__":
    main()
