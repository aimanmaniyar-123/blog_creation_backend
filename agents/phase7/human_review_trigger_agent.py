import random
from typing import Dict, Any
from datetime import datetime
from agents.base_agent import BaseAgent

class HumanReviewTriggerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Human Review Trigger Agent", "Editing, Validation & Proofreading")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content_id = input_data.get("content_id", "")
        trigger_reason = input_data.get("trigger_reason", "complex content")
        reviewer_roles = ["Editor", "Subject Matter Expert"]

        review_ticket = {
            "id": f"HR-{random.randint(1000,9999)}",
            "content_id": content_id,
            "assigned_roles": reviewer_roles,
            "trigger_reason": trigger_reason,
            "timestamp": datetime.now().isoformat()
        }

        return {
            "review_ticket": review_ticket,
            "review_requested": True,
            "recommendations": ["Ensure human reviewer validates nuanced context"],
            "generation_confidence": random.uniform(0.9,0.98)
        }
