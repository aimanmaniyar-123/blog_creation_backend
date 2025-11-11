from typing import Dict, Any
from agents.base_agent import BaseAgent

class IncrementalFunctionAgent(BaseAgent):
    def __init__(self):
        super().__init__("Incremental Function Agent", "Auxiliary")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        current_value = input_data.get("current_value", 0)
        increment = input_data.get("increment", 1)
        new_value = current_value + increment
        return {"new_value": new_value, "status": "done"}
