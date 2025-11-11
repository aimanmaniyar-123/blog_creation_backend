from typing import Dict, Any, List
import re

from agents.base_agent import BaseAgent

def _claim_sentences(text: str) -> List[str]:
    # naive sentence split and claim heuristic (contains numbers or citation-like cues)
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sents if re.search(r"\d|(according to|study|report|source)", s, re.I)]

class AIHallucinationDetectionAgent(BaseAgent):
    """
    Flags likely AI hallucinations by finding claims without provided references.
    """
    def __init__(self):
        super().__init__("AI Hallucination Detection Agent", "Originality")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        provided_sources = set([s.strip().lower() for s in input_data.get("sources", [])])
        claims = _claim_sentences(content)
        unsupported = []
        for c in claims:
            has_marker = bool(re.search(r"\[\d+\]|\(.*\d{4}.*\)|doi:|arxiv:", c, re.I))
            if not has_marker:
                unsupported.append(c)
        hallucination_detected = len(unsupported) > 0 and len(provided_sources) == 0
        return {
            "hallucination_detected": hallucination_detected,
            "unsupported_claims": unsupported[:10],
            "status": "done"
        }
