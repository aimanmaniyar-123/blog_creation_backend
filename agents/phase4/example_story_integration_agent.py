from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class ExampleStoryIntegrationAgent(BaseAgent):
    def __init__(self):
        super().__init__("Example/Story Integration Agent", "Drafting & Content Generation")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        examples = input_data.get("examples", [])

        # Simulate integration of examples or stories
        integrated_content = content + "\n\nExamples:\n"
        for i, example in enumerate(examples, 1):
            integrated_content += f"{i}. {example}\n"

        integration_score = random.uniform(75, 95)

        return {
            "integrated_content": integrated_content.strip(),
            "integration_score": integration_score,
            "status": "Example/story integration complete"
        }
