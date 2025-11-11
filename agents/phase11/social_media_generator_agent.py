from typing import Dict, Any
from agents.base_agent import BaseAgent

class SocialMediaGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Social Media Generator Agent", "Promotion")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        topic = input_data.get("topic", "")
        return {"content": f"Social media posts generated for {topic}", "status": "done"}
