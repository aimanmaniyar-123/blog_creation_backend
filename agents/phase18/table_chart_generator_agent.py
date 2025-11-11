from typing import Dict, Any
from agents.base_agent import BaseAgent

class TableChartGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Table & Chart Generator Agent", "Auxiliary")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data = input_data.get("data", [])
        generated_content = {"table": "HTML table", "chart": "Chart SVG"}
        return {"generated_content": generated_content, "status": "done"}
