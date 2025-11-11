import random
from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class PollPopupSuggestionAgent(BaseAgent):
    def __init__(self):
        super().__init__("Poll/Popup Suggestion Agent", "Content Enrichment")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        topic = input_data.get("topic", "Topic")

        micro_polls = [
            {"poll_id": f"{topic.lower()}_poll_001", "question": f"What's your biggest challenge with {topic.lower()}?"},
            {"poll_id": f"{topic.lower()}_poll_002", "question": f"What would you prioritize when implementing {topic.lower()}?"}
        ]

        popups = [
            {"popup_id": f"{topic.lower()}_popup_001", "offer": f"Free {topic} implementation checklist", "trigger": {"exit_intent": True}},
            {"popup_id": f"{topic.lower()}_popup_002", "offer": f"Access {topic} ROI calculator", "trigger": {"scroll_depth": "40%"}}
        ]

        ux_guidance = [
            "Keep interactions brief and value-driven",
            "Ensure mobile-friendly interactions and accessibility",
            "Avoid repeated triggers that disrupt reading flow"
        ]

        return {
            "micro_polls": micro_polls,
            "popups": popups,
            "ux_guidance": ux_guidance,
            "expected_interaction_rate": f"{random.randint(8,25)}%"
        }
