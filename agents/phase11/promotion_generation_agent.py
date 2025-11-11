from typing import Dict, Any
from agents.base_agent import BaseAgent

class PromotionGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__("Promotion Generation Agent", "Promotion")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"promotion": "Promotional content generated", "status": "done"}
