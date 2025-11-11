from typing import Dict, Any, List
import math
import re

from agents.base_agent import BaseAgent

def _type_token_ratio(text: str) -> float:
    tokens = re.findall(r"\w+", text.lower())
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)

class OriginalityCheckPlagiarismDetectionAgent(BaseAgent):
    """
    Combines originality scoring (type-token ratio + length factor) with similarity checks (delegated).
    """
    def __init__(self, ideal_len: int = 400):
        super().__init__("Originality Check & Plagiarism Detection Agent", "Originality")
        self.ideal_len = ideal_len

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        max_similarity = float(input_data.get("max_similarity", 0.0))  # allow upstream similarity
        ttr = _type_token_ratio(content)
        length = len(content)
        length_score = 1.0 - min(1.0, abs(length - self.ideal_len) / max(1, self.ideal_len))
        originality_score = max(0.0, min(1.0, 0.6 * ttr + 0.4 * length_score))
        plagiarism_found = max_similarity >= float(input_data.get("similarity_threshold", 0.35))
        return {
            "originality_score": round(originality_score, 4),
            "plagiarism_found": plagiarism_found,
            "signals": {"ttr": round(ttr, 4), "length_score": round(length_score, 4), "max_similarity": round(max_similarity, 4)},
            "status": "done"
        }
