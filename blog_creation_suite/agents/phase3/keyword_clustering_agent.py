from typing import Dict, Any
from agents.base_agent import BaseAgent
import random

class KeywordClusteringAgent(BaseAgent):
    def __init__(self):
        super().__init__("Keyword Clustering Agent", "SEO & Keyword Preparation")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        keywords = input_data.get("keywords", [])
        clusters = {}
        cluster_id = 1

        for kw in keywords:
            if len(clusters) == 0:
                clusters[cluster_id] = [kw]
            else:
                # randomly assign keyword to existing or new cluster
                assigned = False
                for c, kws in clusters.items():
                    if random.random() < 0.5:
                        kws.append(kw)
                        assigned = True
                        break
                if not assigned:
                    cluster_id += 1
                    clusters[cluster_id] = [kw]

        return {
            "clusters": clusters,
            "status": "Keyword clustering complete"
        }
