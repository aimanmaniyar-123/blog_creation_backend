from typing import Dict, Any, List, Tuple
import re

from agents.base_agent import BaseAgent

def _extract_facts(text: str) -> List[str]:
    # naive fact extraction: sentences with numbers or proper nouns
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sents if re.search(r"\d|[A-Z][a-z]{2,}", s)]

def _match_refs(facts: List[str], refs: List[str]) -> List[Tuple[str, bool]]:
    matched = []
    for f in facts:
        key = " ".join(re.findall(r"\w+", f.lower()))[:40]
        ok = any(key[:20] in " ".join(re.findall(r"\w+", r.lower())) for r in refs)
        matched.append((f, ok))
    return matched

class DeepFactReferenceCrossValidationAgent(BaseAgent):
    """
    Extracts naive 'facts' and checks if any user-provided references contain overlapping cues.
    """
    def __init__(self):
        super().__init__("Deep Fact-Reference Cross-Validation Agent", "Originality")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        references: List[str] = input_data.get("reference_texts", [])
        facts = _extract_facts(content)
        matches = _match_refs(facts, references)
        covered = [f for f, ok in matches if ok]
        uncovered = [f for f, ok in matches if not ok]
        coverage = 0.0 if not facts else len(covered) / len(facts)
        return {
            "facts_validated": coverage >= 0.5,
            "coverage": round(coverage, 3),
            "uncovered_facts": uncovered[:10],
            "status": "done"
        }
