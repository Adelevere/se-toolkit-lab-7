import httpx
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class LMSAPIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    async def _get(self, endpoint: str, params: Dict = None) -> Any:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{endpoint}",
                    params=params,
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"GET {endpoint} failed: {e}")
            raise
    
    async def _post(self, endpoint: str) -> Any:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}{endpoint}",
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"POST {endpoint} failed: {e}")
            raise
    
    async def get_items(self) -> List[Dict]:
        return await self._get("/items/")
    
    async def get_learners(self) -> List[Dict]:
        return await self._get("/learners/")
    
    async def get_scores(self, lab: str) -> List[Dict]:
        return await self._get("/analytics/scores", {"lab": lab})
    
    async def get_pass_rates(self, lab: str) -> List[Dict]:
        return await self._get("/analytics/pass-rates", {"lab": lab})
    
    async def get_timeline(self, lab: str) -> List[Dict]:
        return await self._get("/analytics/timeline", {"lab": lab})
    
    async def get_groups(self, lab: str) -> List[Dict]:
        return await self._get("/analytics/groups", {"lab": lab})
    
    async def get_top_learners(self, lab: str, limit: int = 5) -> List[Dict]:
        return await self._get("/analytics/top-learners", {"lab": lab, "limit": limit})
    
    async def get_completion_rate(self, lab: str) -> Dict:
        return await self._get("/analytics/completion-rate", {"lab": lab})
    
    async def trigger_sync(self) -> Dict:
        return await self._post("/pipeline/sync")
