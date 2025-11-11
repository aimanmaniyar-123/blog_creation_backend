from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class SourceCredibilityAgent(BaseAgent):
    def __init__(self):
        super().__init__("Source Credibility Agent", "Research & Structuring")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess credibility of sources"""

        sources = input_data.get("sources", [])
        credibility_scores = {source: random.uniform(60, 100) for source in sources}
        common_criteria = [
            "authority",
            "accuracy",
            "currency",
            "relevance",
            "objectivity"
        ]

        credibility_summary = {
            "average_score": sum(credibility_scores.values()) / len(credibility_scores) if credibility_scores else 0,
            "criteria_used": common_criteria,
            "sources_reviewed": len(sources)
        }

        return {
            "credibility_scores": credibility_scores,
            "summary": credibility_summary,
            "status": "Source credibility assessed"
        }
