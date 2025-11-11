from typing import Dict, Any
from agents.base_agent import BaseAgent

class PollCommentAgent(BaseAgent):
    def __init__(self):
        super().__init__("Poll & Comment Agent", "Feedback")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        poll_data = input_data.get("poll_data", {})
        comment_data = input_data.get("comment_data", {})
        status = "processed" if poll_data or comment_data else "no_data"
        return {"poll_status": status, "status": "done"}
