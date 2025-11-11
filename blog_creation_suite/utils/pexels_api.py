import requests
import asyncio
from typing import Dict, List, Optional
from config.settings import SETTINGS

class PexelsAPI:
    def __init__(self):
        self.api_key = SETTINGS.get("PEXELS_API_KEY")
        self.base_url = "https://api.pexels.com/v1"
        self.headers = {"Authorization": self.api_key}

    async def search_images(self, query: str, per_page: int = 5, page: int = 1) -> Dict:
        """Search for images using Pexels API"""

        if not self.api_key or self.api_key == "YOUR_PEXELS_API_KEY":
            # Return mock data if API key not configured
            return self.get_mock_response(query, per_page)

        try:
            url = f"{self.base_url}/search"
            params = {
                "query": query,
                "per_page": per_page,
                "page": page
            }

            response = requests.get(url, headers=self.headers, params=params, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Pexels API error: {response.status_code}")
                return self.get_mock_response(query, per_page)

        except Exception as e:
            print(f"Error calling Pexels API: {e}")
            return self.get_mock_response(query, per_page)

    def get_mock_response(self, query: str, per_page: int) -> Dict:
        """Generate mock Pexels response for development"""

        mock_photos = []
        for i in range(per_page):
            photo_id = 123456 + i
            mock_photos.append({
                "id": photo_id,
                "width": 1920,
                "height": 1080,
                "url": f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg",
                "photographer": f"Mock Photographer {i+1}",
                "photographer_url": f"https://www.pexels.com/@photographer{i+1}",
                "photographer_id": 1000 + i,
                "avg_color": "#374151",
                "src": {
                    "original": f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg",
                    "large2x": f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
                    "large": f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
                    "medium": f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&h=350",
                    "small": f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&h=130"
                },
                "liked": False,
                "alt": f"Professional image related to {query}"
            })

        return {
            "page": 1,
            "per_page": per_page,
            "photos": mock_photos,
            "total_results": 500,
            "next_page": f"https://api.pexels.com/v1/search/?page=2&per_page={per_page}&query={query}"
        }

    def get_image_info(self, photo_id: int) -> Optional[Dict]:
        """Get detailed information about a specific photo"""

        if not self.api_key or self.api_key == "YOUR_PEXELS_API_KEY":
            return None

        try:
            url = f"{self.base_url}/photos/{photo_id}"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except Exception as e:
            print(f"Error getting photo info: {e}")
            return None

    def download_image(self, image_url: str, filename: str) -> bool:
        """Download image from Pexels URL"""

        try:
            response = requests.get(image_url, timeout=30)

            if response.status_code == 200:
                with open(filename, 'wb') as file:
                    file.write(response.content)
                return True
            else:
                return False

        except Exception as e:
            print(f"Error downloading image: {e}")
            return False
