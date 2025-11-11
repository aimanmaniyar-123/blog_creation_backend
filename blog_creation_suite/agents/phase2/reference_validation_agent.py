from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class ReferenceValidationAgent(BaseAgent):
    def __init__(self):
        super().__init__("Reference Validation Agent", "Research & Structuring")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate references in research"""

        references = input_data.get("references", [])
        valid_references = [ref for ref in references if self.is_valid_reference(ref)]
        invalid_references = [ref for ref in references if ref not in valid_references]

        validation_summary = {
            "total_references": len(references),
            "valid_references": len(valid_references),
            "invalid_references": len(invalid_references),
            "validation_rate": (len(valid_references) / len(references)) * 100 if references else 0
        }

        return {
            "valid_references": valid_references,
            "invalid_references": invalid_references,
            "validation_summary": validation_summary,
            "status": "References validated"
        }

    def is_valid_reference(self, reference: str) -> bool:
        # Simplified validation logic: check if reference string length > 5
        return len(reference) > 5
