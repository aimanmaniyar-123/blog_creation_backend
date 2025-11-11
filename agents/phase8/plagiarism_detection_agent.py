from typing import Dict, Any, List, Tuple
import random
import re

from agents.base_agent import BaseAgent

def _shingle(text: str, k: int = 5) -> List[str]:
    tokens = re.findall(r"\w+", text.lower())
    return [" ".join(tokens[i:i+k]) for i in range(max(0, len(tokens)-k+1))]

def _jaccard(a: List[str], b: List[str]) -> float:
    A, B = set(a), set(b)
    if not A and not B:
        return 0.0
    return len(A & B) / max(1, len(A | B))

class PlagiarismDetectionAgent(BaseAgent):
    """
    Heuristic plagiarism detector using k-shingles + Jaccard similarity and length checks.
    """
    def __init__(self, similarity_threshold: float = 0.35):
        super().__init__("Plagiarism Detection Agent", "Originality")
        self.similarity_threshold = similarity_threshold

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        references: List[str] = input_data.get("reference_texts", [])
        k = int(input_data.get("k", 5))
        shingles_c = _shingle(content, k)
        max_sim, best_ref = 0.0, None
        for ref in references:
            sim = _jaccard(shingles_c, _shingle(ref, k))
            if sim > max_sim:
                max_sim, best_ref = sim, ref
        plagiarism_found = max_sim >= self.similarity_threshold
        return {
            "plagiarism_found": plagiarism_found,
            "max_similarity": round(max_sim, 4),
            "best_match_present": best_ref is not None,
            "status": "done"
        }
