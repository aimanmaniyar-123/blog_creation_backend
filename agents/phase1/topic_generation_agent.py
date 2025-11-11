from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class TopicGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__("Topic Generation Agent", "Ideation & Planning")
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        seed = input_data.get("seed", "")
        generated_topics = [f"{seed} Topic {i}" for i in range(1, 6)]
        return {
            "generated_topics": generated_topics
        }