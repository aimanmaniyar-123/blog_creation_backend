import random
from typing import Dict, Any
from agents.base_agent import BaseAgent

class FeedbackModerationAgent(BaseAgent):
    def __init__(self):
        super().__init__("Feedback Moderation Agent", "Feedback")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        feedback = input_data.get("feedback", "")
        moderated = random.choice([True, False])
        return {"moderated": moderated, "status": "done"}
