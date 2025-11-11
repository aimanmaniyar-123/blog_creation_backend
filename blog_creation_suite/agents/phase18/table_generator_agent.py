from typing import Dict, Any
from agents.base_agent import BaseAgent

class TableGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Table Generator Agent", "Auxiliary")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data = input_data.get("data", [])
        table_html = "<table><tr><th>Column 1</th><th>Column 2</th></tr></table>"
        return {"table_html": table_html, "status": "done"}
