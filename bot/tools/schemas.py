import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Tool schemas for LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get list of all labs and tasks in the course",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get list of enrolled students and their groups",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution (4 buckets) for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average scores and attempt counts for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submissions per day for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group scores and student counts for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top N learners by score for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01'"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of top learners to return (default: 5)"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate percentage for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier, e.g., 'lab-01'"
                    }
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Trigger ETL sync to refresh data from autochecker",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

async def execute_tool(lms_client, tool_name: str, arguments: Dict[str, Any]) -> Any:
    """Execute a tool call and return result"""
    logger.info(f"Executing tool: {tool_name}({arguments})")
    
    if tool_name == "get_items":
        return await lms_client.get_items()
    elif tool_name == "get_learners":
        return await lms_client.get_learners()
    elif tool_name == "get_scores":
        return await lms_client.get_scores(arguments.get("lab"))
    elif tool_name == "get_pass_rates":
        return await lms_client.get_pass_rates(arguments.get("lab"))
    elif tool_name == "get_timeline":
        return await lms_client.get_timeline(arguments.get("lab"))
    elif tool_name == "get_groups":
        return await lms_client.get_groups(arguments.get("lab"))
    elif tool_name == "get_top_learners":
        return await lms_client.get_top_learners(
            arguments.get("lab"),
            arguments.get("limit", 5)
        )
    elif tool_name == "get_completion_rate":
        return await lms_client.get_completion_rate(arguments.get("lab"))
    elif tool_name == "trigger_sync":
        return await lms_client.trigger_sync()
    else:
        raise ValueError(f"Unknown tool: {tool_name}")
