from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class ContextGatheringAgent(BaseAgent):
    def __init__(self):
        super().__init__("Context Gathering Agent", "Ideation & Planning")
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        context = input_data.get("context", "")
        return {
            "context_collected": context
        }