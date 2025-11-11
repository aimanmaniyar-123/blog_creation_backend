from typing import Dict, Any
from agents.base_agent import BaseAgent

class NewsletterContentGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Newsletter Content Generator Agent", "Promotion")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"newsletter": "Newsletter content generated", "status": "done"}
