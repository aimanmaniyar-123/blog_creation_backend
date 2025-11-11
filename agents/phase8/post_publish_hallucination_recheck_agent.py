from typing import Dict, Any, Optional
import time

from agents.base_agent import BaseAgent

class PostPublishHallucinationRecheckAgent(BaseAgent):
    """
    Lightweight recheck that can be scheduled post-publish; compares a stored hash or timestamp.
    """
    def __init__(self):
        super().__init__("Post-Publish Hallucination Recheck Agent", "Originality")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        content_id: str = input_data.get("content_id", "")
        last_checked: Optional[float] = input_data.get("last_checked_ts")
        now = time.time()
        stale = (last_checked is None) or (now - float(last_checked) > 24*3600)
        # For demo purposes, we just mark rechecked when stale
        hallucination_rechecked = stale
        return {
            "content_id": content_id,
            "hallucination_rechecked": hallucination_rechecked,
            "next_check_after_sec": 24*3600,
            "status": "done"
        }
