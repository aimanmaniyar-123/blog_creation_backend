from typing import Dict, Any, List
import re

from agents.base_agent import BaseAgent

def _factual_triggers(text: str) -> List[str]:
    # identify sentences containing named entities or dates (naive regex)
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sents if re.search(r"(19|20)\d{2}|[A-Z][a-z]{2,}", s)]

class ContentHallucinationDetectionAgent(BaseAgent):
    """
    Content-level hallucination heuristics: detects specific factual-looking sentences lacking context.
    """
    def __init__(self):
        super().__init__("Content Hallucination Detection Agent", "Originality")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        triggers = _factual_triggers(content)
        suspicious = [s for s in triggers if len(s.split()) > 4 and not re.search(r"http[s]?://|\[[0-9]+\]", s)]
        return {
            "hallucination_detected": len(suspicious) > 0,
            "suspicious_sentences": suspicious[:10],
            "status": "done"
        }
