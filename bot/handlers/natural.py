import json
import logging
import sys
from typing import Dict, Any

from services.llm_client import LLMClient
from tools import TOOLS, execute_tool
from config import Config

logger = logging.getLogger(__name__)

async def handle_natural_query(lms_client, user_message: str) -> str:
    """Handle natural language query with tool calling"""
    try:
        # Initialize LLM client
        llm = LLMClient(
            Config.LLM_API_BASE_URL,
            Config.LLM_API_KEY,
            Config.LLM_API_MODEL
        )
        
        # Step 1: Get LLM response with tool calls
        response = await llm.route_intent(user_message, TOOLS)
        message = response["choices"][0]["message"]
        
        # Check if LLM wants to call tools
        if message.get("tool_calls"):
            # Execute all tool calls
            tool_results = []
            for tool_call in message["tool_calls"]:
                tool_name = tool_call["function"]["name"]
                arguments = json.loads(tool_call["function"]["arguments"])
                
                # Debug output to stderr
                print(f"[tool] LLM called: {tool_name}({arguments})", file=sys.stderr)
                
                # Execute tool
                result = await execute_tool(lms_client, tool_name, arguments)
                tool_results.append({
                    "tool_call_id": tool_call["id"],
                    "role": "tool",
                    "content": json.dumps(result, ensure_ascii=False)
                })
                
                # Debug output
                if isinstance(result, list):
                    print(f"[tool] Result: {len(result)} items", file=sys.stderr)
                else:
                    print(f"[tool] Result: {result}", file=sys.stderr)
            
            # Step 2: Send tool results back to LLM
            messages = [
                {"role": "system", "content": "You are an LMS assistant. Answer based on the tool results."},
                {"role": "user", "content": user_message},
                message,
                *tool_results
            ]
            
            print(f"[summary] Feeding {len(tool_results)} tool results back to LLM", file=sys.stderr)
            
            final_response = await llm.chat(messages)
            return final_response["choices"][0]["message"]["content"]
        
        # No tool calls - just return the response
        return message.get("content", "I'm not sure how to help. Try /help for available commands.")
    
    except Exception as e:
        logger.error(f"Natural query failed: {e}")
        return f"Sorry, I encountered an error: {e}"
