from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class ImageRightsAgent(BaseAgent):
    def __init__(self):
        super().__init__("Image Rights Agent", "Content Enrichment")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        image_source = input_data.get("image_source", "")
        intended_use = input_data.get("intended_use", "commercial")

        guidance = {
            "check_license_terms": True,
            "preferred_sources": ["Pexels", "Unsplash", "Licensed stock providers"],
            "attribution_recommendation": "Include photographer credit where required",
            "model_release_needed": intended_use == "commercial"
        }

        steps = [
            "Identify original source and licensing terms",
            "Check if attribution is required",
            "Check for model/property releases for identifiable people or private property",
            "Retain evidence of license for audit"
        ]

        return {
            "image_source": image_source,
            "guidance": guidance,
            "steps": steps
        }
