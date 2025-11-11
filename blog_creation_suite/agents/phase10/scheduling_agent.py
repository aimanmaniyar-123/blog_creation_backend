from typing import Dict, Any
from agents.base_agent import BaseAgent

class SchedulingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Scheduling Agent", "Scheduling")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        schedule = input_data.get("schedule", {})
        return {"schedule": schedule, "status": "done"}
