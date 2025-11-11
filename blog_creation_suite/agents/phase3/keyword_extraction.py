from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class KeywordExtractionAgent(BaseAgent):
    def __init__(self):
        super().__init__("Keyword Extraction Agent", "SEO & Keyword Preparation")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract keywords relevant to the topic"""

        topic = input_data.get("topic", "")
        text_corpus = input_data.get("text_corpus", "")

        # Mock keyword extraction
        keywords = [f"{topic} keyword {i}" for i in range(1, 11)]
        keyword_metrics = {k: random.uniform(0.1, 1.0) for k in keywords}

        return {
            "keywords": keywords,
            "keyword_metrics": keyword_metrics,
            "status": "Keyword extraction completed"
        }
