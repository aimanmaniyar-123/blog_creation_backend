from typing import Dict, Any
from agents.base_agent import BaseAgent

class ReviewCollectionAgent(BaseAgent):
    def __init__(self):
        super().__init__("Review Collection Agent", "Feedback")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        reviews = input_data.get("reviews", [])
        count = len(reviews)
        return {"review_count": count, "status": "done"}
