from typing import Dict, Any
from agents.base_agent import BaseAgent

class TagCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Tag Checker Agent", "Auxiliary")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        tags = input_data.get("tags", [])
        valid_tags = [tag for tag in tags if len(tag) > 2]  # Simple validation
        return {"valid_tags": valid_tags, "status": "done"}
