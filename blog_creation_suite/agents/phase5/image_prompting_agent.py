from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class ImagePromptingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Image Prompting Agent", "Content Enrichment")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        topic = input_data.get("topic", "Topic")
        styles = input_data.get("styles", ["photorealistic", "editorial", "flat-illustration"])
        aspect_ratios = input_data.get("aspect_ratios", ["16:9", "4:3"])

        prompts: List[str] = []
        for style in styles:
            for ar in aspect_ratios:
                prompts.append(f"{topic} in {style} style, composition focused on people and process, aspect ratio {ar}, high resolution, clean background")

        alt_texts = [f"{topic} related image showing people and process ({s})" for s in styles]

        return {
            "prompts": prompts,
            "alt_texts": alt_texts,
            "recommendation": "Use clear alt-text and photographer credit. Match style to section tone."
        }
