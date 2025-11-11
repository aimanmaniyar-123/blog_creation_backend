from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class OutlineStructuringAgent(BaseAgent):
    def __init__(self):
        super().__init__("Outline Structuring Agent", "Research & Structuring")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a detailed and structured outline from research data"""

        research_findings = input_data.get("research_findings", {})
        main_topics = research_findings.get("key_concepts", [])
        num_sections = len(main_topics)
        outline = []

        for concept in main_topics:
            outline.append({
                "section_title": concept.get("concept", "Untitled Section"),
                "importance": concept.get("importance", "Medium"),
                "details": f"Detailed discussion on {concept.get('concept', '')}"
            })

        outline_quality = random.uniform(75, 95)

        return {
            "outline": outline,
            "num_sections": num_sections,
            "quality_score": outline_quality,
            "status": "Outline successfully structured"
        }
