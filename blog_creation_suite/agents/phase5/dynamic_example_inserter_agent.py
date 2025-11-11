import random
from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class DynamicExampleInserterAgent(BaseAgent):
    def __init__(self):
        super().__init__("Dynamic Example Inserter Agent", "Content Enrichment")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        topic = input_data.get("topic", "Topic")
        audience_level = input_data.get("audience_level", "intermediate")

        success_case_studies = [
            {
                "example_id": f"{topic.lower()}_case_001",
                "title": f"Fortune 500 Company Transforms Operations with {topic}",
                "industry": random.choice(["Technology", "Healthcare", "Manufacturing", "Finance"]),
                "results": {"efficiency_gain": f"{random.randint(25,60)}%", "cost_savings": f"${random.randint(5,50)}M"}
            },
            {
                "example_id": f"{topic.lower()}_case_002",
                "title": f"Startup Scales Rapidly Using {topic} Innovation",
                "industry": "Technology Startup",
                "results": {"growth_acceleration": f"{random.randint(100,300)}%"}
            }
        ]

        micro_examples = [
            {"example": f"Team reduced implementation time by 50% using automated {topic.lower()} workflows", "length": "1 sentence"},
            {"example": f"Department saw 200% ROI within 6 months of {topic.lower()} adoption", "length": "1 sentence"}
        ]

        return {
            "success_case_studies": success_case_studies,
            "micro_examples": micro_examples,
            "total_examples_available": len(success_case_studies) + len(micro_examples),
            "recommended_insertion_points": [
                f"After introducing {topic} core concepts",
                f"Within {topic} benefits discussion",
                f"Before {topic} section conclusions"
            ],
            "generation_confidence": random.uniform(0.86, 0.95)
        }
