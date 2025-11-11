from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class AudiencePersonaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Audience Persona Agent", "Ideation & Planning")
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        persona = input_data.get("persona", "")
        details = {"age": 30, "interests": ["tech", "gaming"]}
        return {
            "persona_details": details
        }