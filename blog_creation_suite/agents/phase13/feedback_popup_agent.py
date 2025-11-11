from typing import Dict, Any
from agents.base_agent import BaseAgent

class FeedbackPopupAgent(BaseAgent):
    def __init__(self):
        super().__init__("Feedback Popup Agent", "Feedback")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        popup_displayed = True
        return {"popup_displayed": popup_displayed, "status": "done"}
