from typing import Dict, Any
from agents.base_agent import BaseAgent

class FormattingPreviewAgent(BaseAgent):
    def __init__(self):
        super().__init__("Formatting Preview Agent", "Scheduling")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        preview_url = "http://example.com/preview"
        return {"preview_url": preview_url, "status": "done"}
