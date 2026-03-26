"""LMS API client."""

import httpx
from config import settings


class LMSClient:
    """Client for interacting with the LMS backend API."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = base_url or settings.lms_api_url
        self.api_key = api_key or settings.lms_api_key
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=30.0,
        )

    async def get_health(self) -> dict:
        """Get backend health status."""
        response = await self._client.get("/docs")
        response.raise_for_status()
        return {"status": "healthy", "url": self.base_url}

    async def get_items(self) -> list[dict]:
        """Get all items (labs) from the LMS."""
        response = await self._client.get("/items/")
        response.raise_for_status()
        return response.json()

    async def get_analytics(self) -> list[dict]:
        """Get analytics data from the LMS."""
        response = await self._client.get("/analytics/")
        response.raise_for_status()
        return response.json()

    async def sync_data(self) -> dict:
        """Trigger data sync from autochecker."""
        response = await self._client.post("/sync/")
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
