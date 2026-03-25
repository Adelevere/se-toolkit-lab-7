import httpx
import logging

logger = logging.getLogger(__name__)

class LMSAPIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    async def check_health(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/items/",
                    headers=self.headers,
                    timeout=5.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return False
    
    async def get_items(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/items/",
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get items: {e}")
            return []
