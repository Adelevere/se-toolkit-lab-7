import logging

logger = logging.getLogger(__name__)

async def start():
    return "Welcome to LMS Bot!\n\nCommands:\n/start\n/help\n/health\n/labs"

async def help_command():
    return "Commands:\n/start - welcome\n/help - this help\n/health - backend status\n/labs - list labs"

async def health(lms_api_client):
    try:
        status = await lms_api_client.check_health()
        return "Backend is healthy" if status else "Backend returned unexpected response"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return "Backend is not reachable"

async def labs(lms_api_client):
    try:
        items = await lms_api_client.get_items()
        if not items:
            return "No labs found"
        lab_list = [f"- {item.get('title', 'Untitled')}" for item in items[:10]]
        return "Available labs:\n" + "\n".join(lab_list)
    except Exception as e:
        logger.error(f"Failed to fetch labs: {e}")
        return "Failed to fetch labs"
