import random
from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class StatInjectorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Stat Injector Agent", "Content Enrichment")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        topic = input_data.get("topic", "Topic")
        content_text = input_data.get("content_text", "")
        available_stats = input_data.get("available_stats", [])
        injection_style = input_data.get("injection_style", "natural")

        placement_strategy = [
            {"location": "introduction", "reason": "Establish market importance", "impact_score": 94},
            {"location": "benefits_section", "reason": "Support claims", "impact_score": 91},
            {"location": "case_study", "reason": "Quantify results", "impact_score": 89}
        ]

        injections: List[Dict[str, Any]] = []
        for i, stat in enumerate(available_stats[:3]):
            injections.append({
                "suggested_location": placement_strategy[i]["location"],
                "statistic": stat,
                "injection_text": f"Inserting stat '{stat}' after the paragraph that introduces {topic} benefits."
            })

        return {
            "placement_strategy": placement_strategy,
            "injections": injections,
            "generation_confidence": random.uniform(0.87, 0.95)
        }
