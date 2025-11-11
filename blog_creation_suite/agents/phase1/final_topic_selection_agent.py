from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class FinalTopicSelectionAgent(BaseAgent):
    def __init__(self):
        super().__init__("Final Topic Selection Agent", "Ideation & Planning")
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        candidate_topics = input_data.get("candidate_topics", [])
        weighted_scores = {topic: random.uniform(0, 100) for topic in candidate_topics}
        sorted_topics = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)
        selected = sorted_topics[0][0] if sorted_topics else None
        rationale = {topic: f"Score: {score}" for topic, score in weighted_scores.items()}
        return {
            "selected_topic": selected,
            "ranking": sorted_topics,
            "rationale": rationale,
        }