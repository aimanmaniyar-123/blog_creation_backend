from typing import Dict, Any
from agents.base_agent import BaseAgent

class TagFixingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Tag Fixing Agent", "Auxiliary")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        tags = input_data.get("tags", [])
        fixed_tags = [tag.lower() for tag in tags]  # Simple normalization example
        return {"fixed_tags": fixed_tags, "status": "done"}
