from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class BrainstormingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Brainstorming Agent", "Core System & Learning")
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        topic = input_data.get("topic", "")
        ideas = [f"Idea {i} about {topic}" for i in range(1, 6)]
        return {
            "ideas": ideas
        }
