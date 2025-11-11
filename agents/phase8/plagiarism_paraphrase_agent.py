from typing import Dict, Any
import re

from agents.base_agent import BaseAgent

def _simple_paraphrase(text: str) -> str:
    # very lightweight paraphrase rules (placeholder)
    rules = {
        r"utilize": "use",
        r"commence": "begin",
        r"terminate": "end",
        r"subsequently": "then",
        r"prior to": "before",
    }
    out = text
    for pat, repl in rules.items():
        out = re.sub(pat, repl, out, flags=re.IGNORECASE)
    return out

class PlagiarismParaphraseAgent(BaseAgent):
    """
    Applies simple lexical substitutions to reduce obvious overlap.
    """
    def __init__(self):
        super().__init__("Plagiarism Paraphrase Agent", "Originality")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        paraphrased_content = _simple_paraphrase(content)
        changed = paraphrased_content != content
        return {"paraphrased_content": paraphrased_content, "changed": changed, "status": "done"}
