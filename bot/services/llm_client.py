import httpx
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def chat(self, messages: List[Dict], tools: List[Dict] = None) -> Dict:
        """Send chat completion request"""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.1
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"LLM chat failed: {e}")
            raise
    
    async def route_intent(self, user_message: str, tools: List[Dict]) -> Dict:
        """Route user message to tools"""
        messages = [
            {
                "role": "system",
                "content": "You are an assistant for a Learning Management System. "
                           "Use the available tools to answer user questions about labs, scores, and learners. "
                           "If the user asks about labs or data, call the appropriate tools. "
                           "If the user says hello, just respond with a greeting. "
                           "If you don't understand, say so and suggest /help."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        return await self.chat(messages, tools)
