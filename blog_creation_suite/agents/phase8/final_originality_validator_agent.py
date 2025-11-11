from typing import Dict, Any

from agents.base_agent import BaseAgent

class FinalOriginalityValidatorAgent(BaseAgent):
    """
    Final gate: ensures originality_score above threshold and no plagiarism flag.
    """
    def __init__(self, min_originality: float = 0.55):
        super().__init__("Final Originality Validator Agent", "Originality")
        self.min_originality = min_originality

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        originality_score = float(input_data.get("originality_score", 0.0))
        plagiarism_found = bool(input_data.get("plagiarism_found", False))
        valid = (originality_score >= self.min_originality) and (not plagiarism_found)
        return {"valid_originality": valid, "threshold": self.min_originality, "status": "done"}
