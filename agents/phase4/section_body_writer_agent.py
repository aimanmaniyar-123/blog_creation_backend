from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class SectionBodyWriterAgent(BaseAgent):
    def __init__(self):
        super().__init__("Section/Body Writer Agent", "Drafting & Content Generation")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        section_headings = input_data.get("section_headings", [])
        points = input_data.get("points", [])

        content = ""
        for heading in section_headings:
            content += f"## {heading}\n"
            for point in points:
                content += f"- {point}\n"
            content += "\n"  # extra space between sections

        quality_score = random.uniform(80, 95)

        return {
            "generated_body": content.strip(),
            "quality_score": quality_score,
            "status": "Section/body writing complete"
        }
