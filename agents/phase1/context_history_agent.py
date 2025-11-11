from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class ContextHistoryAgent(BaseAgent):
    def __init__(self):
        super().__init__("Context History Agent", "Ideation & Planning")
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        history = input_data.get("history", [])
        return {
            "context_history": history[:10]
        }