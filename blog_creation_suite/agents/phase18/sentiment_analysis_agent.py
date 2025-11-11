import random
from typing import Dict, Any
from agents.base_agent import BaseAgent

class SentimentAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("Sentiment Analysis Agent", "Auxiliary")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content = input_data.get("content", "")
        sentiment = random.choice(["positive", "neutral", "negative"])
        return {"sentiment": sentiment, "status": "done"}
