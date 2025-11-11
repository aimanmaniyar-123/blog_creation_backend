import random
from typing import Dict, Any
from agents.base_agent import BaseAgent

class ChatbotAgent(BaseAgent):
    def __init__(self):
        super().__init__("Chatbot Agent", "Feedback")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_input = input_data.get("user_input", "")
        response = f"Simulated chatbot response to: {user_input}"
        return {"chatbot_response": response, "status": "done"}
