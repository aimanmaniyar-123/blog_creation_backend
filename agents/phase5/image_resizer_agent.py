from typing import Dict, Any
from agents.base_agent import BaseAgent
from PIL import Image, ImageOps
import io

class ImageResizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Image Resizer Agent", "Content Enrichment")

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        image_bytes = input_data.get("image_bytes")
        target_size = input_data.get("target_size", (800, 450))
        preserve_aspect = input_data.get("preserve_aspect", True)

        result = {"resized_bytes": None, "target_size": target_size, "error": None}
        if not image_bytes:
            result["error"] = "No image bytes provided."
            return result

        try:
            img = Image.open(io.BytesIO(image_bytes))
            img = img.convert("RGB")
            if preserve_aspect:
                img.thumbnail(target_size, Image.Resampling.LANCZOS)
            else:
                img = ImageOps.fit(img, target_size, Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=85, optimize=True)
            result["resized_bytes"] = buf.getvalue()
            return result
        except Exception as e:
            result["error"] = str(e)
            return result
