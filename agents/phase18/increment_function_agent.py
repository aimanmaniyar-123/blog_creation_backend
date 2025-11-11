from typing import Dict, Any
from agents.base_agent import BaseAgent

class IncrementFunctionAgent(BaseAgent):
    def __init__(self):
        super().__init__("Increment Function Agent", "Auxiliary")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        value = input_data.get("value", 0)
        incremented_value = value + 1
        return {"incremented_value": incremented_value, "status": "done"}
