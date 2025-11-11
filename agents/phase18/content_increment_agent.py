from typing import Dict, Any
from agents.base_agent import BaseAgent

class ContentIncrementAgent(BaseAgent):
    def __init__(self):
        super().__init__("Content Increment Agent", "Auxiliary")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content_version = input_data.get("content_version", 1)
        new_version = content_version + 1
        return {"new_version": new_version, "status": "done"}
