from typing import Dict, Any, List
from agents.base_agent import BaseAgent

class MultimediaEmbedAgent(BaseAgent):
    def __init__(self):
        super().__init__("Multimedia Embed Agent", "Content Enrichment")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        embeds: List[Dict[str, str]] = []
        if "video_url" in input_data:
            embeds.append({
                "type": "video",
                "html": f'<div class="video-embed"><iframe src="{input_data["video_url"]}" frameborder="0" allowfullscreen></iframe></div>',
                "recommendation": "Make iframe responsive with CSS wrappers"
            })
        if "tweet_url" in input_data:
            embeds.append({
                "type": "tweet",
                "html": f'<blockquote class="twitter-tweet"><a href="{input_data["tweet_url"]}"></a></blockquote>',
                "recommendation": "Load Twitter embed script async and lazy-load when visible"
            })
        if "slides_url" in input_data:
            embeds.append({
                "type": "slides",
                "html": f'<iframe src="{input_data["slides_url"]}" class="slides-embed" frameborder="0"></iframe>',
                "recommendation": "Limit height and lazy-load when in viewport"
            })

        return {
            "embeds": embeds,
            "recommendation": "Use responsive wrappers and lazy-loading for media to preserve UX"
        }
