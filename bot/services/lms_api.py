import httpx
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class LMSAPIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    async def get_items(self) -> List[Dict[str, Any]]:
        """Get all items (labs and tasks)"""
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
            raise
    
    async def get_pass_rates(self, lab_id: str) -> List[Dict[str, Any]]:
        """Get pass rates for a specific lab"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/analytics/pass-rates",
                    params={"lab": lab_id},
                    headers=self.headers,
                    timeout=10.0
                )
                if response.status_code == 404:
                    return []
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to get pass rates for {lab_id}: {e}")
            raise
