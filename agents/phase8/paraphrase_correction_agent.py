from typing import Dict, Any
import re

from agents.base_agent import BaseAgent

def _fix_common_issues(text: str) -> str:
    # simplify whitespace, fix spacing around punctuation, collapse repeats
    t = re.sub(r"\s+", " ", text).strip()
    t = re.sub(r"\s+([,.;:!?])", r"", t)
    t = re.sub(r"([.!?]){3,}", r"", t)
    return t

class ParaphraseCorrectionAgent(BaseAgent):
    """
    Cleans paraphrased content to improve readability and style consistency.
    """
    def __init__(self):
        super().__init__("Paraphrase Correction Agent", "Originality")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        corrected_content = _fix_common_issues(content)
        changed = corrected_content != content
        return {"corrected_content": corrected_content, "changed": changed, "status": "done"}
