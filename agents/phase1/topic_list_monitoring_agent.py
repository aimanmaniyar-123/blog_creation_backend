from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class TopicListMonitoringAgent(BaseAgent):
    def __init__(self):
        super().__init__("Topic List Monitoring Agent", "Ideation & Planning")
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        topics = input_data.get("topics", [])
        return {
            "monitored_topics": topics
        }