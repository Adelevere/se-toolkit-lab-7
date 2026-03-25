# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)

async def start():
    return "Welcome to LMS Bot!\n\nI can help you track your progress in the Software Engineering Toolkit course.\n\nTry /help to see available commands."

async def help_command():
    return (
        "Available Commands\n\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/health - Check backend status\n"
        "/labs - List all available labs\n"
        "/scores <lab_name> - Get pass rates for a lab\n\n"
        "Examples:\n"
        "/scores lab-01\n"
        "/scores Lab 02"
    )

async def health(lms_api_client):
    """Check backend health"""
    try:
        items = await lms_api_client.get_items()
        if items:
            return f"Backend is healthy. {len(items)} items available."
        else:
            return "Backend is reachable but returned no data. Run ETL sync."
    except Exception as e:
        error_msg = str(e)
        if "Connection refused" in error_msg or "ConnectError" in error_msg:
            return "Backend error: connection refused (localhost:42002). Check that the services are running."
        elif "401" in error_msg or "Unauthorized" in error_msg:
            return "Backend error: unauthorized. Check LMS_API_KEY in .env.bot.secret."
        else:
            return f"Backend error: {error_msg}"

async def labs(lms_api_client):
    """List all labs"""
    try:
        items = await lms_api_client.get_items()
        if not items:
            return "No labs found. Run ETL sync first."
        
        labs_list = []
        for item in items:
            if item.get('type') == 'lab':
                labs_list.append(f"- {item['title']}")
        
        if not labs_list:
            return "No labs found."
        
        return "Available Labs:\n\n" + "\n".join(labs_list)
    except Exception as e:
        logger.error(f"Failed to fetch labs: {e}")
        return f"Failed to fetch labs: {e}"

async def scores(lms_api_client, lab_name: str):
    """Get pass rates for a specific lab"""
    if not lab_name:
        return "Please specify a lab name.\nExample: /scores lab-01"
    
    try:
        # Clean lab name (remove spaces, convert to lowercase)
        lab_id = lab_name.lower().strip().replace(' ', '-')
        if not lab_id.startswith('lab-'):
            lab_id = f"lab-{lab_id}"
        
        pass_rates = await lms_api_client.get_pass_rates(lab_id)
        
        if not pass_rates:
            return f"No data found for {lab_name}. Check lab name or run ETL sync."
        
        result = f"Pass Rates for {lab_name}\n\n"
        for task in pass_rates:
            task_name = task.get('task', 'Unknown')
            avg_score = task.get('avg_score', 0)
            attempts = task.get('attempts', 0)
            result += f"- {task_name}: {avg_score:.1f}% ({attempts} attempts)\n"
        
        return result
    except Exception as e:
        logger.error(f"Failed to fetch scores: {e}")
        return f"Failed to fetch scores: {e}"
